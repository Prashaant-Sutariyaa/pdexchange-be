from pydantic_settings import BaseSettings
from pathlib import Path


class Settings(BaseSettings):
    DATABASE_URL: str
    EXCHANGE_DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    APP_NAME: str = "SaaSApp"
    ENVIRONMENT: str = "development"

    graph_tenant_id: str

    graph_client_id: str

    graph_client_secret: str

    graph_sender_email: str

    class Config:
        env_file = Path(__file__).resolve().parent.parent.parent / ".env"


settings = Settings()
