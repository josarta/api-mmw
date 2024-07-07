from typing import List
from fastapi import APIRouter, status , Depends
import httpx
from sqlalchemy import func
from config.db import session
from models.location import locations
from schemas.location import Location , LocationCount
from circuit_breaker.config import circuit_breaker
from config.db import BASE_URL
import urllib.parse
from routes.token import User , get_current_active_user

category = APIRouter();

@circuit_breaker
async def call_api(url: str):
    endpoint = BASE_URL
    encoded_url = urllib.parse.quote(url)
    url = f"http://{endpoint}/api/v1/locations?url={encoded_url}"
    async with httpx.AsyncClient(timeout=2) as client:
        r = await client.get(url)
        return endpoint, r.text
    

location = APIRouter();

@location.get("/api/v1/locations", 
   tags=["Locations"],
    response_model=List[Location],
    description="Get a list of all locations",)
async def get_all_locations(current_user: User = Depends(get_current_active_user)):
     return session.query(locations).all();


@location.get("/api/v1/locations/count", 
              tags=["Locations"], 
              description="Return count of avaliable locations",
              response_model=LocationCount)
async def get_locations_count(current_user: User = Depends(get_current_active_user)):
    result = session.query(func.count(locations.c.location_id)).scalar()
    return {"total": result}



@location.post("/api/v1/locations", 
   tags=["Locations"],
    response_model=Location,
    description="Add new location.",)
async def create_new_locations(location:Location, current_user: User = Depends(get_current_active_user)):
     new_location = {"latitude": location.latitude, "longitude": location.longitude}
     result = session.execute(locations.insert().values(new_location))
     session.commit()
     return session.execute(locations.select().where(locations.c.location_id == result.lastrowid)).first()


@location.get(
    "/api/v1/locations/{id}",
    tags=["Locations"],
     response_model=Location,
     description="Get a single location by id.")
async def get_location(id: str, current_user: User = Depends(get_current_active_user)):
     return session.execute(locations.select().where(locations.c.location_id == id)).first()


@location.put(
    "/api/v1/locations/{id}",  
    tags=["Locations"], 
    response_model=Location, 
    description="Update a location by Id")
async def update_location(location:Location, id: int, current_user: User = Depends(get_current_active_user)):
    session.execute(
        locations.update()
        .values(latitude = location.latitude , longitude= location.longitude)
        .where(locations.c.location_id== id)
    )
    session.commit()
    return session.execute(locations.select().where(locations.c.location_id == id)).first()


@location.delete(
          "/api/v1/locations/{id}", 
          tags=["Locations"], 
          status_code= status.HTTP_204_NO_CONTENT)
async def delete_location(id: int, current_user: User = Depends(get_current_active_user)):
    session.execute(locations.delete().where(locations.c.location_id == id))
    session.commit()
    return session.execute(locations.select().where(locations.c.location_id == id)).first()

