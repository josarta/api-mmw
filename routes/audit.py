from typing import List
from fastapi import APIRouter
from sqlalchemy import func
from config.db import session
from models.audit import audits
from schemas.audit import Audit , AuditCount


audit = APIRouter();


@audit.get("/audit", 
   tags=["Audit"],
    response_model=List[Audit],
    description="Get a list of all audit",)
async def get_all_audit():
     return session.query(audits).all();


@audit.get("/audit/count", 
              tags=["Audit"], 
              description="Return count of avaliable audit",
              response_model=AuditCount)
async def get_audit_count():
    result = session.query(func.count(audits.c.audit_id)).scalar()
    return {"total": result}


