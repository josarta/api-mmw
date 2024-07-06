from typing import Optional
from pydantic import BaseModel
from pymysql import Timestamp

class Location(BaseModel):
    location_id: Optional[int]
    latitude: float
    longitude: float
    created_at: Optional[Timestamp] # type: ignore

class LocationCount(BaseModel):
    total: int 
