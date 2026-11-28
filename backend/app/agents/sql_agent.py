import re
from typing import Any

from langchain_community.agent_toolkits.sql.base import create_sql_agent
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain_groq import ChatGroq

from app.agents.prompts import TECHSTORE_SYSTEM_PROMPT
from app.core.config import settings
from app.database.connection import get_db
from app.schema.query import AgentStep, QueryResponse


def get_agent_executor():
    api_key = settings.api_key
    if not api_key:
        raise ValueError(
            "Ni GROQ_API_KEY ni LLM_API_KEY están configuradas en las variables de entorno."
        )

    db = get_db()

    llm = ChatGroq(
        model=settings.llm_model or "openai/gpt-oss-120b",
        groq_api_key=api_key,
        temperature=0.0,
    )

    toolkit = SQLDatabaseToolkit(db=db, llm=llm)

    agent_executor = create_sql_agent(
        llm=llm,
        toolkit=toolkit,
        verbose=True,
        agent_type="tool-calling",
        prefix=TECHSTORE_SYSTEM_PROMPT,
        agent_executor_kwargs={"return_intermediate_steps": True},
        max_iterations=10,
    )

    return agent_executor


def extract_sql_query(intermediate_steps: list[Any]) -> str | None:
    for action, _observation in reversed(intermediate_steps):
        tool = getattr(action, "tool", "")
        tool_input = getattr(action, "tool_input", None)

        if isinstance(tool_input, dict) and "query" in tool_input:
            return str(tool_input["query"]).strip()

        if isinstance(tool_input, str) and any(
            kw in tool_input.upper() for kw in ("SELECT", "WITH", "FROM")
        ):
            return tool_input.strip()

        if "query" in str(tool).lower() and tool_input:
            if isinstance(tool_input, dict):
                return str(tool_input.get("query", tool_input)).strip()
            return str(tool_input).strip()

    return None


def run_techstore_agent(question: str) -> QueryResponse:
    try:
        agent_executor = get_agent_executor()
        result = agent_executor.invoke({"input": question})

        answer = result.get("output", "")
        raw_steps = result.get("intermediate_steps", [])

        formatted_steps: list[AgentStep] = []
        for i, (action, obs) in enumerate(raw_steps, 1):
            formatted_steps.append(
                AgentStep(
                    step_number=i,
                    action=getattr(action, "tool", "Thought/Action"),
                    action_input=getattr(action, "tool_input", None),
                    observation=str(obs)[:500] if obs is not None else None,
                )
            )

        sql_query = extract_sql_query(raw_steps)
        if not sql_query:
            match = re.search(
                r"```sql\s*(SELECT[\s\S]*?);?\s*```", answer, re.IGNORECASE
            )
            if match:
                sql_query = match.group(1).strip()

        return QueryResponse(
            question=question,
            answer=answer,
            sql_query=sql_query,
            steps=formatted_steps,
            success=True,
        )
    except Exception as e:
        return QueryResponse(
            question=question,
            answer=f"Error al procesar la consulta con el agente: {str(e)}",
            sql_query=None,
            steps=[],
            success=False,
            error=str(e),
        )
