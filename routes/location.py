from typing import List
from fastapi import APIRouter, status
from sqlalchemy import func
from config.db import session
from models.location import locations
from schemas.location import Location , LocationCount

location = APIRouter();


@location.get("/locations", 
   tags=["Locations"],
    response_model=List[Location],
    description="Get a list of all locations",)
async def get_all_locations():
     return session.query(locations).all();


@location.get("/locations/count", 
              tags=["Locations"], 
              description="Return count of avaliable locations",
              response_model=LocationCount)
async def get_locations_count():
    result = session.query(func.count(locations.c.location_id)).scalar()
    return {"total": result}



@location.post("/locations", 
   tags=["Locations"],
    response_model=Location,
    description="Add new location.",)
async def create_new_locations(location:Location):
     new_location = {"latitude": location.latitude, "longitude": location.longitude}
     result = session.execute(locations.insert().values(new_location))
     session.commit()
     return session.execute(locations.select().where(locations.c.location_id == result.lastrowid)).first()


@location.get(
    "/locations/{id}",
    tags=["Locations"],
     response_model=Location,
     description="Get a single location by id.")
async def get_location(id: str):
     return session.execute(locations.select().where(locations.c.location_id == id)).first()


@location.put(
    "/locations/{id}",  
    tags=["Locations"], 
    response_model=Location, 
    description="Update a location by Id")
async def update_location(location:Location, id: int):
    session.execute(
        locations.update()
        .values(latitude = location.latitude , longitude= location.longitude)
        .where(locations.c.location_id== id)
    )
    session.commit()
    return session.execute(locations.select().where(locations.c.location_id == id)).first()


@location.delete(
          "/locations/{id}", 
          tags=["Locations"], 
          status_code= status.HTTP_204_NO_CONTENT)
async def delete_location(id: int):
    session.execute(locations.delete().where(locations.c.location_id == id))
    session.commit()
    return session.execute(locations.select().where(locations.c.location_id == id)).first()

