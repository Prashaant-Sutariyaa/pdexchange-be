from sqlalchemy import create_engine
from sqlalchemy.engine import Engine


POSTGRES_URL = (
    "postgresql+psycopg2://postgres:930766@localhost:5432/backend_db"
)


def get_postgres_engine() -> Engine:
    return create_engine(POSTGRES_URL)