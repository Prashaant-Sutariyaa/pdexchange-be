from pydantic import BaseModel
from typing import Dict, Optional


class MappingCreate(BaseModel):

    # 🔥 CUSTOM SOURCE QUERY
    source_query: str

    dest_table: str

    timestamp_col: str

    column_mappings: Dict[str, str]


class MappingResponse(BaseModel):

    id: int

    source_query: str

    dest_table: str

    timestamp_col: str

    column_mappings: Dict[str, str]

    last_sync_position: Optional[str] = None

    rows_synced: int = 0

    last_synced: Optional[str] = None