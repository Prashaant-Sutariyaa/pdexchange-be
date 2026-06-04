from sqlalchemy import text

# ============================================================
# 🔥 LOOKUP CONFIG
# ============================================================
LOOKUP_CONFIG = {
    "role_id": {"table": "roles", "key": "name"},
    "department_id": {"table": "departments", "key": "name"},
    "campaign_id": {"table": "campaigns", "key": "campaign_code"},
    "client_id": {"table": "clients", "key": "client_code"},
}


# ============================================================
# 🔥 LOAD REQUIRED LOOKUPS
# ============================================================
def load_required_lookups(postgres_conn, column_mappings):

    required_lookups = {}

    for dest_col in column_mappings.values():

        if dest_col not in LOOKUP_CONFIG:
            continue

        config = LOOKUP_CONFIG[dest_col]

        table = config["table"]

        key = config["key"]

        query = f"""
            SELECT id, {key}
            FROM {table}
        """

        rows = postgres_conn.execute(text(query)).mappings().all()

        required_lookups[dest_col] = {row[key]: row["id"] for row in rows}

    return required_lookups
