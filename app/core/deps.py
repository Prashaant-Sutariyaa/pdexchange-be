from app.db.session import (
    SessionLocal,
    ExchangeSessionLocal
)

def get_db():
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


def get_exchange_db():
    db = ExchangeSessionLocal()

    try:
        yield db

    finally:
        db.close()