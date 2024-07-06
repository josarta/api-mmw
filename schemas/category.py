from typing import Optional
from pydantic import BaseModel
from pymysql import Timestamp


class OrmBaseModel(BaseModel):
    class Config:
        orm_mode = True

class Category(OrmBaseModel):
    category_id: Optional[int]
    name: str
    created_at: Optional[Timestamp] # type: ignore

class CategoryCount(BaseModel):
    total: int 