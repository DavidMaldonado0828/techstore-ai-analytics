from fastapi import APIRouter

from app.schema.query import QueryRequest, QueryResponse
from app.services.query_service import process_query

router = APIRouter()


@router.post("/queries", response_model=QueryResponse)
def query(request: QueryRequest) -> QueryResponse:
    answer = process_query(request.question)

    return QueryResponse(question=request.question, answer=answer)
