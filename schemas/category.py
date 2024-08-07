from typing import Optional
from pydantic import BaseModel
from pymysql import Timestamp


class OrmBaseModel(BaseModel):
    class Config:
        orm_mode = True


class Category(OrmBaseModel):
    category_id: Optional[int] | None = 0
    name: str | None = ""
    created_at: Optional[Timestamp] | None = None  # type: ignore


class CategoryCount(BaseModel):
    total: int
