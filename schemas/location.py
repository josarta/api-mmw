from decimal import Decimal
from typing import Optional
from pydantic import BaseModel
from pymysql import Timestamp


class OrmBaseModel(BaseModel):
    class Config:
        orm_mode = True


class Location(OrmBaseModel):
    location_id: Optional[int] | None = 0
    latitude: Decimal | None = 0
    longitude: Decimal | None = 0
    created_at: Optional[Timestamp] | None = None  # type: ignore


class LocationCount(BaseModel):
    total: int
