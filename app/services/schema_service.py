from sqlalchemy import inspect, text

from app.core.mysql_client import get_mysql_engine
from app.core.postgres_client import get_postgres_engine


# ============================================================
# 🔹 MYSQL TABLES
# ============================================================
def get_mysql_tables():

    engine = get_mysql_engine()

    inspector = inspect(engine)

    tables = inspector.get_table_names()

    result = []

    with engine.connect() as conn:

        for table in tables:

            columns = inspector.get_columns(table)

            timestamp_col = None

            for col in columns:
                if col["name"] in ["updated_on", "modified_on"]:
                    timestamp_col = col["name"]

            count = conn.execute(
                text(f"SELECT COUNT(*) FROM {table}")
            ).scalar()

            result.append({
                "name": table,
                "row_count": count,
                "columns": [
                    {
                        "name": c["name"],
                        "type": str(c["type"])
                    }
                    for c in columns
                ],
                "timestamp_col": timestamp_col,
            })

    return result


# ============================================================
# 🔹 POSTGRES TABLES
# ============================================================
def get_postgres_tables():

    engine = get_postgres_engine()

    inspector = inspect(engine)

    print(inspector.get_schema_names())

    tables = inspector.get_table_names(schema="public")

    print(tables)

    result = []

    with engine.connect() as conn:

        current_db = conn.execute(
            text("SELECT current_database()")
        ).scalar()

        print(current_db)

        for table in tables:

            columns = inspector.get_columns(
                table,
                schema="public"
            )

            count = conn.execute(
                text(f'SELECT COUNT(*) FROM "{table}"')
            ).scalar()

            result.append({
                "name": table,
                "row_count": count,
                "columns": [
                    {
                        "name": c["name"],
                        "type": str(c["type"])
                    }
                    for c in columns
                ],
            })

    return result