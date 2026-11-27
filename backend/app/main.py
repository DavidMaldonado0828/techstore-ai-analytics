from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import api_router
from app.core.config import get_settings

settings = get_settings()

app = FastAPI(
    title=settings.APP_NAME,
    description="""
## TechStore AI Analytics API

Esta API permite consultar en lenguaje natural el modelo dimensional Gold de **TechStore** alojado en **Neon PostgreSQL**.

### Características:
- **Usuario de Solo Lectura:** Conexión segura con permisos estrictos de `SELECT`.
- **Agente SQL:** Desarrollado con **LangChain** y **Groq** (`llama-3.1-8b-instant`).
- **CAG (Context-Augmented Generation):** Esquema dimensional de 8 tablas y Reglas de Negocio inyectadas en el prompt.
- **Trazabilidad:** Devuelve la consulta SQL generada y cada uno de los pasos de razonamiento del agente.
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configuración de CORS para permitir peticiones desde el frontend (React / Next.js)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir las rutas de la versión 1
app.include_router(api_router, prefix="/api/v1")


@app.get("/", tags=["Root"])
def root():
    return {
        "message": "Bienvenido a TechStore AI Analytics API",
        "docs": "/docs",
        "health": "/api/v1/health",
        "query": "/api/v1/query",
    }
