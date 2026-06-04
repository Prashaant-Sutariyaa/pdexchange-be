from pydantic import BaseModel
from typing import Optional


class VendorCreate(BaseModel):
    name: str
    address: Optional[str]
    country: Optional[str]
    assigned_to: int

    contract_file_name: Optional[str]
    contract_file: Optional[str]

    first_name: Optional[str]
    last_name: Optional[str]
    contact_designation: Optional[str]
    contact_email: Optional[str]
    contact_office_number: Optional[str]
    contact_mobile_number: Optional[str]

    billing_name: Optional[str]
    billing_address: Optional[str]
    billing_email: Optional[str]
    billing_terms: Optional[str]


class VendorUpdate(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    country: Optional[str] = None
    assigned_to: Optional[int] = None

    contract_file_name: Optional[str] = None
    contract_file: Optional[str] = None

    first_name: Optional[str] = None
    last_name: Optional[str] = None
    contact_designation: Optional[str] = None
    contact_email: Optional[str] = None
    contact_office_number: Optional[str] = None
    contact_mobile_number: Optional[str] = None

    billing_name: Optional[str] = None
    billing_address: Optional[str] = None
    billing_email: Optional[str] = None
    billing_terms: Optional[str] = None

    is_active: Optional[bool] = None