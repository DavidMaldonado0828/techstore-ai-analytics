from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class QueryRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    question: str = Field(min_length=3, max_length=1000)


class AgentStep(BaseModel):
    step_number: int
    action: str
    action_input: Any
    observation: str | None = None


class QueryResponse(BaseModel):
    question: str
    answer: str
    sql_query: str | None = None
    steps: list[AgentStep] = Field(default_factory=list)
    success: bool = True
    error: str | None = None
