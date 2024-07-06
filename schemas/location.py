from typing import Optional
from pydantic import BaseModel
from pymysql import Timestamp

class OrmBaseModel(BaseModel):
    class Config:
        orm_mode = True


class Location(OrmBaseModel):
    location_id: Optional[int]
    latitude: float
    longitude: float
    created_at: Optional[Timestamp] # type: ignore

class LocationCount(BaseModel):
    total: int     