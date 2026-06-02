from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    BUCKET_NAME: str
    REGION_NAME: str
    AWS_ENDPOINT_URL: Optional[str] = None
    STORAGE_PUBLIC_BASE_URL: Optional[str] = None

    model_config = SettingsConfigDict(
        env_file='.env', env_file_encoding='utf-8'
    )
