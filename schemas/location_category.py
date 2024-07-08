from re import L
from typing import Optional
from unicodedata import category
from pydantic import BaseModel
from schemas.category import Category
from schemas.location import Location
from pymysql import Timestamp

class OrmBaseModel(BaseModel):
    class Config:
        orm_mode = True

class JsonLocationCategory(OrmBaseModel):
    review_id: Optional[int]  | None = 0
    reviewed_at: Optional[Timestamp]  | None = None # type: ignore
    category: Optional[Category]  | None = Category()
    location: Optional[Location] | None =  Location()
    

class LocationCategory(OrmBaseModel):
    review_id: Optional[int]
    reviewed_at: Optional[Timestamp] # type: ignore
    location_id: Optional[int]
    latitude: float
    longitude: float
    category_id: Optional[int]
    name: str | None = ""

class LocationCategoryIn(OrmBaseModel):
    location_id: Optional[int]
    category_id: Optional[int]
    
class LocationCategoryCount(BaseModel):
    total: int 

#    [Column('review_id', INTEGER(), table=<location_category_reviewed>, primary_key=True, nullable=False), Column('location_id', INTEGER(), ForeignKey('locations.location_id'), table=<location_category_reviewed>, nullable=False), Column('category_id', INTEGER(), ForeignKey('categories.category_id'), table=<location_category_reviewed>, nullable=False), Column('reviewed_at', TIMESTAMP(), table=<location_category_reviewed>, server_default=DefaultClause(<sqlalchemy.sql.elements.TextClause object at 0x00000213494FECC0>, for_update=False))]

 