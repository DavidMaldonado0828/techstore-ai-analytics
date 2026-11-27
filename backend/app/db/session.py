from langchain_community.utilities import SQLDatabase
from sqlalchemy import create_engine, text

from app.core.config import get_settings

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
    settings = get_settings()
    if not settings.DATABASE_URL:
        raise ValueError(
            "DATABASE_URL no está configurada en las variables de entorno."
        )

    return create_engine(
        settings.DATABASE_URL,
        pool_pre_ping=True,
        pool_size=5,
        max_overflow=10,
    )


def test_db_connection() -> dict:
    engine = get_engine()
    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT current_user, current_database(), version();")
        ).fetchone()
        return {
            "status": "connected",
            "user": result[0],
            "database": result[1],
            "version": result[2],
        }


def get_sql_database() -> SQLDatabase:
    settings = get_settings()
    if not settings.DATABASE_URL:
        raise ValueError(
            "DATABASE_URL no está configurada en las variables de entorno."
        )

    return SQLDatabase.from_uri(
        database_uri=settings.DATABASE_URL,
        include_tables=GOLD_TABLES,
        sample_rows_in_table_info=2,
    )
