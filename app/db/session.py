from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings  # adjust import path if needed

engine = create_engine(settings.DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Exchange Database
exchange_engine = create_engine(
    settings.EXCHANGE_DATABASE_URL
)

ExchangeSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=exchange_engine
)