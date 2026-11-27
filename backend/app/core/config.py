from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(
    BaseSettings
):  # BaseSettings es una clase de Pydantic que permite obtener configuraciones de entorno y variables de entorno de manera sencilla.
    app_name: str = "TechStore AI Analytics"
    app_env: str = "development"

    database_url: str | None = None
    llm_api_key: str | None = None
    llm_model: str | None = None

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
