from typing import Optional
from pydantic import BaseModel
from pymysql import Timestamp
from sqlalchemy import text

class Category(BaseModel):
    category_id: Optional[int]
    name: str
    created_at: Optional[Timestamp] # type: ignore

class CategoryCount(BaseModel):
    total: int 
    
class CategoryDelete(BaseModel):
    state: text