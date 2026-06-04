from datetime import datetime

from app.core.json_manager import (
    load_mappings,
    save_mappings,
)


# ============================================================
# 🔹 GET MAPPINGS
# ============================================================
def get_mappings():
    return load_mappings()


# ============================================================
# 🔹 CREATE MAPPING
# ============================================================
from app.core.json_manager import (
    load_mappings,
    save_mappings,
)


# ============================================================
# 🔥 CREATE MAPPING
# ============================================================
def create_mapping(data):

    mappings = load_mappings()

    mapping_list = mappings["mappings"]

    new_id = 1

    if mapping_list:
        new_id = max(m["id"] for m in mapping_list) + 1

    new_mapping = {
        "id": new_id,
        "source_query": data.source_query,
        "dest_table": data.dest_table,
        "timestamp_col": data.timestamp_col,
        "column_mappings": data.column_mappings,
        "last_sync_position": None,
        "rows_synced": 0,
        "last_synced": None,
    }

    mapping_list.append(new_mapping)

    save_mappings(mappings)

    return new_mapping


# ============================================================
# 🔹 DELETE MAPPING
# ============================================================
def delete_mapping(mapping_id: int):

    mappings = load_mappings()

    mappings["mappings"] = [m for m in mappings["mappings"] if m["id"] != mapping_id]

    save_mappings(mappings)

    return True
