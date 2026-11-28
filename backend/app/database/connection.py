from langchain_community.utilities import SQLDatabase
from sqlalchemy import create_engine, text

from app.core.config import settings

GOLD_TABLES = [
    "dim_branch",
    "dim_customer",
    "dim_date",
    "dim_payment_method",
    "dim_product",
    "fact_sales",
    "fact_warranties",
    "fact_returns",
]


def get_engine():
    if not settings.database_url:
        raise RuntimeError("DATABASE_URL no está configurada")

    database_url = settings.database_url.replace(
        "postgresql://",
        "postgresql+psycopg://",
        1,
    )

    return create_engine(
        database_url,
        pool_pre_ping=True,
    )


def get_db() -> SQLDatabase:
    engine = get_engine()
    return SQLDatabase(
        engine,
        include_tables=GOLD_TABLES,
        sample_rows_in_table_info=2,
    )


def test_connection() -> dict:
    engine = get_engine()
    with engine.connect() as connection:
        result = connection.execute(
            text("SELECT current_user, current_database(), version();")
        ).fetchone()
        return {
            "status": "connected",
            "user": result[0],
            "database": result[1],
            "version": result[2],
        }


# Instancia lazy para retrocompatibilidad
_db = None


def __getattr__(name: str):
    global _db
    if name == "db":
        if _db is None:
            _db = get_db()
        return _db
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
