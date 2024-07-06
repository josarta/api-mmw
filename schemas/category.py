from typing import Optional
from pydantic import BaseModel
from pymysql import Timestamp

class Category(BaseModel):
    category_id: Optional[int]
    name: str
    created_at: Optional[Timestamp] # type: ignore

class CategoryCount(BaseModel):
    total: int 
