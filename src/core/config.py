from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings loaded from the .env file.
    """

    # =========================
    # Application Settings
    # =========================
    app_name: str
    app_version: str
    environment: str = "development"
    debug: bool = True

    # =========================
    # Security Settings
    # =========================
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # =========================
    # Database Settings
    # =========================
    postgres_host: str
    postgres_port: int
    postgres_db: str
    postgres_user: str
    postgres_password: str
    database_url: str

    # =========================
    # CORS Settings
    # =========================
    backend_cors_origins: str = (
        "http://localhost:3000,http://localhost:8000"
    )

    # =========================
    # Logging Settings
    # =========================
    log_level: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    """
    Return a cached Settings instance.
    """

    return Settings()  # type: ignore[call-arg]


settings = get_settings()