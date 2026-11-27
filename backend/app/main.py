from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.health import router as health_router
from app.api.routes.queries import router as queries_router
from app.core.config import settings

app = FastAPI(
    title=settings.app_name,
    description="""
## TechStore AI Analytics API

API con agente de inteligencia artificial (LangChain + Groq) para consultar el modelo Gold en Neon PostgreSQL.
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router, prefix="/api/v1")
app.include_router(queries_router, prefix="/api/v1")


@app.get("/", tags=["Root"])
def root():
    return {
        "app": settings.app_name,
        "docs": "/docs",
        "health": "/api/v1/health",
        "queries": "/api/v1/queries",
    }
