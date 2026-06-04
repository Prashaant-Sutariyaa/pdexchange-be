from fastapi import APIRouter

from app.services.schema_service import (
    get_mysql_tables,
    get_postgres_tables,
)

from app.services.mapping_service import (
    get_mappings,
    create_mapping,
    delete_mapping,
)

from app.services.sync_service import sync_all_tables

from app.schemas.sync import MappingCreate


router = APIRouter(prefix="/api", tags=["Sync"])


# ============================================================
# 🔹 MYSQL TABLES
# ============================================================
@router.get("/mysql/tables")
def mysql_tables():
    return get_mysql_tables()


# ============================================================
# 🔹 POSTGRES TABLES
# ============================================================
@router.get("/postgres/tables")
def postgres_tables():
    return get_postgres_tables()


# ============================================================
# 🔹 GET MAPPINGS
# ============================================================
@router.get("/mappings")
def mappings():
    return get_mappings()


# ============================================================
# 🔹 CREATE MAPPING
# ============================================================
@router.post("/mappings")
def add_mapping(data: MappingCreate):
    return create_mapping(data)


# ============================================================
# 🔹 DELETE MAPPING
# ============================================================
@router.delete("/mappings/{mapping_id}")
def remove_mapping(mapping_id: int):
    return delete_mapping(mapping_id)


# ============================================================
# 🔥 SYNC ALL
# ============================================================
@router.post("/sync")
def sync():
    return sync_all_tables()