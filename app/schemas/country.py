from pydantic import BaseModel
from typing import Optional


class CountryCreate(BaseModel):
    name: str
    region: str

    iso3: Optional[str] = None
    iso2: Optional[str] = None

    phonecode: Optional[str] = None

    capital: Optional[str] = None
    currency: Optional[str] = None

    status: Optional[str] = "Active"

    wikidata_id: Optional[str] = None


class CountryUpdate(BaseModel):
    name: Optional[str] = None
    region: Optional[str] = None

    iso3: Optional[str] = None
    iso2: Optional[str] = None

    phonecode: Optional[str] = None

    capital: Optional[str] = None
    currency: Optional[str] = None

    status: Optional[str] = None

    wikidata_id: Optional[str] = None
