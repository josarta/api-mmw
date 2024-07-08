from typing import Optional
from pydantic import BaseModel
from pymysql import Timestamp


class OrmBaseModel(BaseModel):
    class Config:
        orm_mode = True


class Audit(OrmBaseModel):
    audit_id: Optional[int]
    action: str
    entity: str
    entity_id: int
    created_at: Optional[Timestamp]  # type: ignore


class AuditCount(BaseModel):
    total: int
