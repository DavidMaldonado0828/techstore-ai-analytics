from sqlalchemy import create_engine, text

from app.core.config import settings

if not settings.database_url:
    raise RuntimeError("DATABASE_URL no está configurada")

database_url = settings.database_url.replace(
    "postgresql://",
    "postgresql+psycopg://",
    1,
)

engine = create_engine(
    database_url,  # Donde y con que credenciales
    pool_pre_ping=True,  # Comprueba que una conexión siga disponible antes de conectarse
)


def test_connection():
    with engine.connect() as connection:
        """result = connection.execute(
            text("SELECT current_user, current_database()")
        )
        return result.fetchone()
        """
        result = connection.execute(text("SELECT * FROM fact_sales LIMIT 5"))
        return result.fetchall()
