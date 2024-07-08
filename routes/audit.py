from sys import audit
from typing import List
from fastapi import APIRouter, Depends
import httpx
from sqlalchemy import func
from config.db import session
from models.audit import audits
from schemas.audit import Audit, AuditCount
from circuit_breaker.config import circuit_breaker
from config.db import BASE_URL
import urllib.parse
from routes.token import User, get_current_active_user

audit = APIRouter()


@circuit_breaker
async def call_api(url: str):
    endpoint = BASE_URL
    encoded_url = urllib.parse.quote(url)
    url = f"http://{endpoint}/api/v1/scrap?url={encoded_url}"
    async with httpx.AsyncClient(timeout=2) as client:
        r = await client.get(url)
        return endpoint, r.text


@audit.get(
    "/api/v1/audit",
    tags=["Audit"],
    response_model=List[Audit],
    description="Get a list of all audit",
)
async def get_all_audit(current_user: User = Depends(get_current_active_user)):
    """returns the information automatically when a category or location is created

    Args:
        current_user (User, optional): _description_. Defaults to Depends(get_current_active_user).

    Returns:
        List[Audit]: return a list of the stored information
    """
    return session.query(audits).all()


@audit.get(
    "/api/v1/audit/count",
    tags=["Audit"],
    description="Return count of avaliable audit",
    response_model=AuditCount,
)
async def get_audit_count(current_user: User = Depends(get_current_active_user)):
    """return the amount records of stored information

    Args:
        current_user (User, optional): _description_. Defaults to Depends(get_current_active_user).

    Returns:
        int : Total amount records of stored information
    """
    result = session.query(func.count(audits.c.audit_id)).scalar()
    return {"total": result}
