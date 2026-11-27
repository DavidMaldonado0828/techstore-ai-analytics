from fastapi import FastAPI

from app.api.routes.health import router as health_router
from app.api.routes.queries import router as queries_router
from app.core.config import settings

app = FastAPI(title=settings.app_name)  # Servicio web

app.include_router(health_router, prefix="/api/v1")
app.include_router(queries_router, prefix="/api/v1")
