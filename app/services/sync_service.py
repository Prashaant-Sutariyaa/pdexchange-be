from datetime import datetime

from sqlalchemy import text

from app.core.mysql_client import get_mysql_engine
from app.core.postgres_client import get_postgres_engine

from app.core.json_manager import (
    load_mappings,
    save_mappings,
)

from app.core.logger import logger

from app.core.lookups import (
    LOOKUP_CONFIG,
    load_required_lookups,
)


# ============================================================
# 🔥 SYNC ALL TABLES
# ============================================================
def sync_all_tables():

    mysql_engine = get_mysql_engine()

    postgres_engine = get_postgres_engine()

    mappings_data = load_mappings()

    mappings = mappings_data["mappings"]

    total_rows = 0

    failed_mappings = []

    start_time = datetime.utcnow()

    # ============================================================
    # 🔥 MYSQL CONNECTION
    # ============================================================
    with mysql_engine.connect() as mysql_conn:

        # ============================================================
        # 🔥 POSTGRES CONNECTION
        # ============================================================
        with postgres_engine.connect() as postgres_conn:

            # ====================================================
            # 🔥 LOOP ALL MAPPINGS
            # ====================================================
            for mapping in mappings:

                try:

                    source_query = mapping["source_query"]

                    dest_table = mapping["dest_table"]

                    timestamp_col = mapping["timestamp_col"]

                    column_mappings = mapping["column_mappings"]

                    last_sync = mapping["last_sync_position"]

                    logger.info(f"SYNC STARTED -> {dest_table}")

                    # ================================================
                    # 🔥 LOAD LOOKUPS
                    # ================================================
                    required_lookups = load_required_lookups(
                        postgres_conn, column_mappings
                    )

                    # ================================================
                    # 🔥 BUILD QUERY
                    # ================================================
                    final_query = source_query

                    params = {}

                    if last_sync:

                        final_query += f"""
                            WHERE {timestamp_col} > :last_sync
                        """

                        params["last_sync"] = last_sync

                    logger.info(final_query)

                    # ================================================
                    # 🔥 FETCH SOURCE ROWS
                    # ================================================
                    rows = (
                        mysql_conn.execute(text(final_query), params).mappings().all()
                    )

                    row_count = len(rows)

                    logger.info(f"ROWS FETCHED: {row_count}")

                    if not rows:

                        logger.info(f"NO NEW ROWS -> {dest_table}")

                        continue

                    # ================================================
                    # 🔥 TRANSFORM ROWS
                    # ================================================
                    transformed_rows = []

                    for row in rows:

                        transformed_row = {}

                        for source_col, dest_col in column_mappings.items():

                            value = row.get(source_col)

                            if isinstance(value, bytes):
                                value = value.decode("utf-8")
                            # ========================================
                            # 🔥 BOOLEAN CONVERSION
                            # ========================================
                            if (
                                dest_col in ["is_active", "is_deleted", "churnable"]
                                and value is not None
                            ):

                                value = bool(value)

                            # ========================================
                            # 🔥 LOOKUP CONVERSION
                            # ========================================
                            if dest_col in LOOKUP_CONFIG:

                                lookup_data = required_lookups.get(dest_col, {})

                                value = lookup_data.get(value)

                            transformed_row[dest_col] = value

                        transformed_rows.append(transformed_row)

                    # ================================================
                    # 🔥 UPSERT QUERY
                    # ================================================
                    dest_columns = list(column_mappings.values())

                    columns_sql = ", ".join(dest_columns)

                    placeholders = ", ".join([f":{c}" for c in dest_columns])

                    # ================================================
                    # 🔥 UPDATE FIELDS
                    # ================================================
                    update_fields = []

                    for col in dest_columns:

                        if col == "id":
                            continue

                        update_fields.append(f"{col} = EXCLUDED.{col}")

                    update_sql = ", ".join(update_fields)

                    insert_query = f"""
                        INSERT INTO "{dest_table}"
                        ({columns_sql})
                        VALUES ({placeholders})

                        ON CONFLICT (id)

                        DO UPDATE SET
                        {update_sql}
                    """

                    logger.info(insert_query)

                    # ================================================
                    # 🔥 EXECUTE UPSERT
                    # ================================================
                    postgres_conn.execute(text(insert_query), transformed_rows)

                    postgres_conn.commit()

                    # ================================================
                    # 🔥 UPDATE WATERMARK
                    # ================================================
                    timestamp_key = timestamp_col.split(".")[-1]

                    latest_timestamp = max(
                        row[timestamp_key] for row in rows if row.get(timestamp_key)
                    )

                    mapping["last_sync_position"] = latest_timestamp.isoformat()

                    # ================================================
                    # 🔥 UPDATE META
                    # ================================================
                    sync_time = datetime.utcnow().isoformat()

                    mapping["last_synced"] = sync_time

                    mapping["rows_synced"] += row_count

                    total_rows += row_count

                    logger.info(f"SYNC COMPLETED -> {dest_table}")

                except Exception as e:

                    postgres_conn.rollback()

                    logger.error(f"SYNC FAILED -> {mapping.get('dest_table')}")

                    logger.error(str(e))

                    failed_mappings.append(
                        {"table": mapping.get("dest_table"), "error": str(e)}
                    )

                    continue

    # ============================================================
    # 🔥 SAVE MAPPINGS
    # ============================================================
    save_mappings(mappings_data)

    duration = str(datetime.utcnow() - start_time)

    return {
        "status": "completed",
        "duration": duration,
        "tables_synced": len(mappings),
        "total_rows": total_rows,
        "failed_mappings": failed_mappings,
    }
