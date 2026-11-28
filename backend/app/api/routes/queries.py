from fastapi import APIRouter

from app.schema.query import QueryRequest, QueryResponse
from app.services.query_service import process_query

router = APIRouter()


@router.post(
    "/queries",
    response_model=QueryResponse,
    summary="Consultar el modelo Gold de TechStore en lenguaje natural",
)
def query(request: QueryRequest) -> QueryResponse:
    return process_query(request.question)
