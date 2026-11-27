from fastapi import APIRouter, HTTPException, status

from app.agent.sql_agent import run_techstore_agent
from app.core.config import get_settings
from app.db.session import test_db_connection
from app.schemas.query import HealthResponse, QueryRequest, QueryResponse

router = APIRouter()


@router.post(
    "/query",
    response_model=QueryResponse,
    summary="Consultar el modelo Gold de TechStore en lenguaje natural",
    description="Recibe una pregunta en español, utiliza un agente SQL con Groq + LangChain para consultar la base de datos de solo lectura en Neon y devuelve la respuesta junto con el SQL y los pasos del agente.",
)
async def query_techstore(request: QueryRequest):
    if not request.question or not request.question.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La pregunta no puede estar vacía.",
        )

    response = run_techstore_agent(request.question)
    return response


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Verificar estado del servicio y conexión a la base de datos Neon",
)
async def health_check():
    settings = get_settings()
    try:
        db_info = test_db_connection()
        return HealthResponse(
            status="healthy",
            database=db_info,
            llm_provider="Groq",
            model=settings.GROQ_MODEL,
        )
    except Exception as e:
        return HealthResponse(
            status="unhealthy",
            database={"error": str(e)},
            llm_provider="Groq",
            model=settings.GROQ_MODEL,
        )
