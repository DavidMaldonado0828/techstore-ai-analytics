from fastapi import APIRouter

from app.core.config import settings
from app.database.connection import test_connection

router = APIRouter()


@router.get("/health", summary="Verificar estado del servicio y conexión a Neon")
def health():
    try:
        db_info = test_connection()
        return {
            "status": "healthy",
            "database": db_info,
            "llm_model": settings.llm_model,
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "database": {"error": str(e)},
            "llm_model": settings.llm_model,
        }
