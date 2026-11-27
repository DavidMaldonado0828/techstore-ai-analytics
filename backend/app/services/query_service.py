from app.agents.sql_agent import run_techstore_agent
from app.schema.query import QueryResponse


def process_query(question: str) -> QueryResponse:
    return run_techstore_agent(question)
