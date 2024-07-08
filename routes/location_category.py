from typing import List
from fastapi import APIRouter, status, Depends
import httpx
from sqlalchemy import func, select, text
from config.db import session
from models.location_category import location_category_reviewed
from schemas.location_category import (
    LocationCategoryCount,
    LocationCategoryIn,
    JsonLocationCategory,
)
from schemas.category import Category
from models.category import categories
from schemas.location import Location
from models.location import locations
from circuit_breaker.config import circuit_breaker
from config.db import BASE_URL
import urllib.parse
from sqlalchemy.orm import Bundle
from routes.token import User, get_current_active_user


QUERY_ALL = "SELECT lc.review_id, lc.reviewed_at, l.location_id , l.latitude, l.longitude , c.category_id , c.name FROM location_category_reviewed as lc inner join categories as c on lc.category_id = c.category_id inner join locations as l on lc.location_id = l.location_id "
QUERY_FITER_LOCATION = "SELECT l.location_id , l.latitude, l.longitude ,l.created_at name FROM location_category_reviewed as lc inner join categories as c on lc.category_id = c.category_id inner join locations as l on lc.location_id = l.location_id "
QUERY_FIND_CATEGORY = "where lc.category_id = "
QUERY_FIND = "where lc.review_id = "
QUERY_EXPLORATION_RECOMMENDER = "SELECT r.review_id, r.reviewed_at, l.location_id, l.latitude, l.longitude, l.created_at, c.category_id, c.name, c.created_at FROM locations l CROSS JOIN categories c LEFT JOIN location_category_reviewed r ON l.location_id = r.location_id AND c.category_id = r.category_id WHERE r.reviewed_at IS NULL OR r.reviewed_at < NOW() - INTERVAL 30 DAY ORDER BY r.reviewed_at IS NULL DESC, r.reviewed_at ASC LIMIT 10"
locationCategoryReviewed = APIRouter()


@circuit_breaker
async def call_api(url: str):
    endpoint = BASE_URL
    encoded_url = urllib.parse.quote(url)
    url = f"http://{endpoint}/api/v1/location-category?url={encoded_url}"
    async with httpx.AsyncClient(timeout=2) as client:
        r = await client.get(url)
        return endpoint, r.text


@locationCategoryReviewed.get(
    "/api/v1/location-category",
    tags=["Location Category Review"],
    response_model=List[JsonLocationCategory],
    description="Get a list of all locations",
)
async def get_location_category_reviews(
    current_user: User = Depends(get_current_active_user),
):
    """_summary_

    Args:
        current_user (User, optional): logged in user token Defaults. Defaults to Depends(get_current_active_user).

    Returns:
        _type_: _description_
    """
    stmt = (
        select(
            location_category_reviewed.c.review_id,
            location_category_reviewed.c.reviewed_at,
            Bundle(
                "category",
                categories.c.category_id,
                categories.c.name,
                categories.c.created_at,
            ),
            Bundle(
                "location",
                locations.c.location_id,
                locations.c.latitude,
                locations.c.longitude,
                locations.c.created_at,
            ),
        )
        .join_from(location_category_reviewed, locations)
        .join_from(location_category_reviewed, categories)
    )
    return session.execute(stmt)


@locationCategoryReviewed.get(
    "/api/v1/location-category/count",
    tags=["Location Category Review"],
    description="Return count of avaliable Location Category Review",
    response_model=LocationCategoryCount,
)
async def get_location_category_reviews_count(
    current_user: User = Depends(get_current_active_user),
):
    """_summary_

    Args:
        current_user (User, optional): logged in user token Defaults. Defaults to Depends(get_current_active_user).

    Returns:
        _type_: _description_
    """
    result = session.query(func.count(location_category_reviewed.c.review_id)).scalar()
    return {"total": result}


@locationCategoryReviewed.post(
    "/api/v1/location-category",
    tags=["Location Category Review"],
    response_model=JsonLocationCategory,
    description="Create and conect location category.",
)
async def create_new_location_category_reviews(
    locationCategoryIn: LocationCategoryIn,
    current_user: User = Depends(get_current_active_user),
):
    """_summary_

    Args:
        locationCategoryIn (LocationCategoryIn): _description_
        current_user (User, optional): logged in user token Defaults. Defaults to Depends(get_current_active_user).

    Returns:
        _type_: _description_
    """
    new_location_category = {
        "location_id": locationCategoryIn.location_id,
        "category_id": locationCategoryIn.category_id,
    }
    result = session.execute(
        location_category_reviewed.insert().values(new_location_category)
    )
    session.commit()
    stmt = (
        select(
            location_category_reviewed.c.review_id,
            location_category_reviewed.c.reviewed_at,
            Bundle(
                "category",
                categories.c.category_id,
                categories.c.name,
                categories.c.created_at,
            ),
            Bundle(
                "location",
                locations.c.location_id,
                locations.c.latitude,
                locations.c.longitude,
                locations.c.created_at,
            ),
        )
        .join_from(location_category_reviewed, locations)
        .join_from(location_category_reviewed, categories)
        .filter(location_category_reviewed.c.review_id == result.lastrowid)
    )
    return session.execute(stmt).first()


@locationCategoryReviewed.get(
    "/api/v1/location-category/{id}",
    tags=["Location Category Review"],
    response_model=JsonLocationCategory,
    description="GET location category by id.",
)
async def get_location_category_reviews(
    id: str, current_user: User = Depends(get_current_active_user)
):
    """ Returns the list of all the categories and locationes stores in the database.

    Args:
        id (str): _description_
        current_user (User, optional): logged in user token Defaults. Defaults to Depends(get_current_active_user).

    Returns:
       JsonLocationCategory: List of the categories and locations
    """
    stmt = (
        select(
            location_category_reviewed.c.review_id,
            location_category_reviewed.c.reviewed_at,
            Bundle(
                "category",
                categories.c.category_id,
                categories.c.name,
                categories.c.created_at,
            ),
            Bundle(
                "location",
                locations.c.location_id,
                locations.c.latitude,
                locations.c.longitude,
                locations.c.created_at,
            ),
        )
        .join_from(location_category_reviewed, locations)
        .join_from(location_category_reviewed, categories)
        .filter(location_category_reviewed.c.review_id == id)
    )
    return session.execute(stmt).first()


#     textual_sql = text(QUERY_ALL + QUERY_FIND + id)
#    return session.execute(textual_sql).first()


@locationCategoryReviewed.put(
    "/api/v1/location-category/{id}",
    tags=["Location Category Review"],
    response_model=JsonLocationCategory,
    description="Update a location category by Id",
)
async def update_location_category(
    locationCategoryIn: LocationCategoryIn,
    id: int,
    current_user: User = Depends(get_current_active_user),
):
    """ Update one of the category and location in the database.

    Args:
        locationCategoryIn (LocationCategoryIn): _description_
        id (int): _description_
        current_user (User, optional): logged in user token Defaults. Defaults to Depends(get_current_active_user).

    Returns:
        _JsonLocationCategory:returns updated category and location
    """
    session.execute(
        location_category_reviewed.update()
        .values(
            location_id=locationCategoryIn.location_id,
            category_id=locationCategoryIn.category_id,
        )
        .where(location_category_reviewed.c.review_id == id)
    )
    session.commit()
    stmt = (
        select(
            location_category_reviewed.c.review_id,
            location_category_reviewed.c.reviewed_at,
            Bundle(
                "category",
                categories.c.category_id,
                categories.c.name,
                categories.c.created_at,
            ),
            Bundle(
                "location",
                locations.c.location_id,
                locations.c.latitude,
                locations.c.longitude,
                locations.c.created_at,
            ),
        )
        .join_from(location_category_reviewed, locations)
        .join_from(location_category_reviewed, categories)
        .filter(location_category_reviewed.c.review_id == id)
    )
    return session.execute(stmt).first()


@locationCategoryReviewed.delete(
    "/api/v1/location-category/{id}",
    tags=["Location Category Review"],
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_location_category(
    id: int, current_user: User = Depends(get_current_active_user)
):
    """emove one of the category and location in the database.

    Args:
        id (int): Key to search category and location in the database.
        current_user (User, optional): logged in user token Defaults. Defaults to Depends(get_current_active_user).

    Returns:
         N/A: --
    """
    session.execute(
        location_category_reviewed.delete().where(
            location_category_reviewed.c.review_id == id
        )
    )
    session.commit()
    textual_sql = text(QUERY_ALL + QUERY_FIND + str(id))
    return session.execute(textual_sql).first()


@locationCategoryReviewed.get(
    "/api/v1/location-category/locations/{id}",
    tags=["Location Category Review"],
    response_model=List[Location],
    description="Return all locations consulting by category",
)
async def get_all_location_consulting_category(
    id: int, current_user: User = Depends(get_current_active_user)
):
    """Return an object with the quantity categories and location stores in the data base consulting by category.

    Args:
        id (int): Key to search category and location in the database.
        current_user (User, optional): logged in user token Defaults. Defaults to Depends(get_current_active_user).

    Returns:
        List[Location] : Return all locations consulting by category
    """
    textual_sql = text(QUERY_FITER_LOCATION + QUERY_FIND_CATEGORY + str(id))
    return session.execute(textual_sql).fetchall()


@locationCategoryReviewed.get(
    "/api/v1/location-category/scan/",
    tags=["Location Category Review"],
    response_model=List[JsonLocationCategory],
    description="Last ten scan recommender",
)
async def get_last_ten_scan_recommender(
    current_user: User = Depends(get_current_active_user),
):
    """Return Last ten scan recommender.
        
    Args:
        current_user (User, optional): logged in user token Defaults. Defaults to Depends(get_current_active_user).

    Returns:
        List[JsonLocationCategory]: Last ten scan recommender
    """
    textual_sql = text(QUERY_EXPLORATION_RECOMMENDER)
    listReturn = []
    print(textual_sql)
    for row in session.execute(textual_sql):
        jsonLocationCategory = JsonLocationCategory()
        jsonLocationCategory.review_id = row.review_id
        jsonLocationCategory.reviewed_at = row.reviewed_at
        jsonC = Category()
        jsonC.category_id = row.category_id
        jsonC.name = row.name
        jsonC.created_at = row.created_at
        jsonL = Location()
        jsonL.location_id = row.location_id
        jsonL.latitude = row.latitude
        jsonL.longitude = row.longitude
        jsonL.created_at = row.created_at
        jsonLocationCategory.category = jsonC
        jsonLocationCategory.location = jsonL
        listReturn.append(jsonLocationCategory)
    return listReturn
