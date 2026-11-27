from langchain.tools import tool

from app.database.connection import db


@tool
def list_tables() -> list[str]:
    """Lista las tablas disponibles en la base de datos."""
    return db.get_usable_table_names()


@tool
def get_schema(table_names: list[str]) -> str:
    """Obtiene las columnas, tipos de datos y estructura de las tablas indicadas."""
    return db.get_table_info(table_names)


@tool
def execute_sql(query: str) -> str:
    """Ejecuta una consulta SQL SELECT en la base de datos y devuelve los resultados."""
    if not query.strip().lower().startswith("select"):
        return "Error: Solo se permiten consultas SELECT."

    try:
        return db.run(query)
    except Exception as e:
        return f"Error ejecutando SQL: {str(e)}"
