from typing import Any

from pydantic import BaseModel, Field


class QueryRequest(BaseModel):
    question: str = Field(
        ...,
        description="Pregunta en lenguaje natural sobre los datos de TechStore",
        example="¿Cuáles son las 5 sucursales con mayores ingresos?",
    )


class AgentStep(BaseModel):
    step_number: int
    action: str
    action_input: Any
    observation: str | None = None


class QueryResponse(BaseModel):
    question: str
    answer: str
    sql_query: str | None = Field(
        None,
        description="Consulta SQL generada y ejecutada por el agente",
    )
    steps: list[AgentStep] = Field(
        default_factory=list,
        description="Pasos intermedios y razonamiento del agente",
    )
    success: bool = True
    error: str | None = None


class HealthResponse(BaseModel):
    status: str
    database: dict
    llm_provider: str
    model: str
