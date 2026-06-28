from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # =========================
    # Application Settings
    # =========================
    app_name: str
    app_version: str

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
    # General Settings
    # =========================
    debug: bool = True

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
