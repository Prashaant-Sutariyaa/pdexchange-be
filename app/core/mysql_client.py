from sqlalchemy import create_engine
from sqlalchemy.engine import Engine


MYSQL_URL = (
    "mysql+pymysql://root:@localhost/pvinecrm"
)


def get_mysql_engine() -> Engine:
    return create_engine(MYSQL_URL)