from pydantic import BaseModel
from typing import Optional


class SentinelJobUploadResponse(BaseModel):
    id: int
    department: str
    file_name: str
    status: str
    priority: str