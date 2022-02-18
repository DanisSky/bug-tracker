import secrets
from typing import Optional, Any

from pydantic import BaseSettings, PostgresDsn, validator


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    ALGORITHM: str

    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_PORT: str
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None

    @validator('SQLALCHEMY_DATABASE_URI', pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme='postgresql',
            user=values.get('POSTGRES_USER'),
            password=values.get('POSTGRES_PASSWORD'),
            host=values.get('POSTGRES_SERVER'),
            port=values.get('POSTGRES_PORT'),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )

    FIRST_MANAGER: str
    FIRST_MANAGER_PASSWORD: str

    class Config:
        env_file = ".env_dev"


settings = Settings()
