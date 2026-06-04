from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str

    mobile_number: Optional[str] = None
    job_title: Optional[str] = None
    work_location: Optional[str] = None

    role_id: int
    department_id: int


class UserUpdate(BaseModel):
    password: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    mobile_number: Optional[str] = None
    job_title: Optional[str] = None
    work_location: Optional[str] = None

    role_id: Optional[int] = None
    department_id: Optional[int] = None

    is_active: Optional[bool] = None


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    first_name: str
    last_name: str

    mobile_number: Optional[str]
    job_title: Optional[str]
    work_location: Optional[str]

    role_id: int
    department_id: int

    is_active: bool
    is_deleted: bool

    created_by: Optional[int]   # ✅ ADD
    updated_by: Optional[int]   # ✅ ADD

    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True