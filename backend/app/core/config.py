from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "TechStore AI Analytics"
    app_env: str = "development"

    database_url: str | None = None
    llm_api_key: str | None = None
    groq_api_key: str | None = None
    llm_model: str = "openai/gpt-oss-120b"

    @property
    def api_key(self) -> str | None:
        return self.groq_api_key or self.llm_api_key

    model_config = SettingsConfigDict(
        env_file=(".env", "backend/.env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
