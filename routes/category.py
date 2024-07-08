from typing import List
from fastapi import APIRouter, HTTPException, status, Depends
import httpx
from sqlalchemy import func
from config.db import session
from models.category import categories
from schemas.category import Category, CategoryCount
from circuit_breaker.config import circuit_breaker
from config.db import BASE_URL
import urllib.parse
from routes.token import User, get_current_active_user

category = APIRouter()


@circuit_breaker
async def call_api(url: str):
    endpoint = BASE_URL
    encoded_url = urllib.parse.quote(url)
    url = f"http://{endpoint}/api/v1/categories?url={encoded_url}"
    async with httpx.AsyncClient(timeout=2) as client:
        r = await client.get(url)
        return endpoint, r.text


@category.get(
    "/api/v1/categories",
    tags=["Categories"],
    response_model=List[Category],
    description="Get a list of all categories",
)
async def get_all_categories(current_user: User = Depends(get_current_active_user)):
    """Returns the list of all the categories stores in the database.

    Args:
        current_user (User, optional): logged in user token Defaults to Depends(get_current_active_user).

    Returns:
        List[Category]: List of the categories
    """
    return session.query(categories).all()


@category.get(
    "/api/v1/categories/count",
    tags=["Categories"],
    description="Return count of avaliable categories",
    response_model=CategoryCount,
)
async def get_categories_count(current_user: User = Depends(get_current_active_user)):
    """Return an object with the quantity categories stores in the data base.

    Args:
        current_user (User, optional):logged in user token. Defaults to Depends(get_current_active_user).

    Returns:
        CategoryCount: retun an object with the quantity categories stores in the database
    """
    result = session.query(func.count(categories.c.category_id)).scalar()
    return {"total": result}


@category.post(
    "/api/v1/categories",
    tags=["Categories"],
    response_model=Category,
    description="Add new category.",
)
async def create_new_categories(
    category: Category, current_user: User = Depends(get_current_active_user)
):
    """Allows the entry of a new category.

    Args:
        category (Category): new data for category
        current_user (User, optional):logged in user token. Defaults to Depends(get_current_active_user).

    Returns:
        Category Object: the new category return
    """
    new_category = {"name": category.name}
    result = session.execute(categories.insert().values(new_category))
    session.commit()
    return session.execute(
        categories.select().where(categories.c.category_id == result.lastrowid)
    ).first()


@category.get(
    "/api/v1/categories/{id}",
    tags=["Categories"],
    response_model=Category,
    description="Get a single tion by id.",
)
async def get_category(id: str, current_user: User = Depends(get_current_active_user)):
    """Recover one of the category in the database.

    Args:
        id (str): Key to search category in the database.
        current_user (User, optional): logged in user token. Defaults to Depends(get_current_active_user).

    Returns:
         Category Object: returns searched category
    """

    gCategory = session.execute(
        categories.select().where(categories.c.category_id == id)
    ).first()
    if gCategory is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No record found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return gCategory


@category.put(
    "/api/v1/categories/{id}",
    tags=["Categories"],
    response_model=Category,
    description="Update a category by Id",
)
async def update_category(
    category: Category, id: int, current_user: User = Depends(get_current_active_user)
):
    """Update one of the category in the database.

    Args:
        category (Category): values ​​to update category
        id (int):  Key to search category in the database.
        current_user (User, optional): logged in user token. Defaults to Depends(get_current_active_user).

    Returns:
          Category Object: returns updated category
    """
    session.execute(
        categories.update()
        .values(name=category.name)
        .where(categories.c.category_id == id)
    )
    session.commit()

    return session.execute(
        categories.select().where(categories.c.category_id == id)
    ).first()


@category.delete(
    "/api/v1/categories/{id}",
    tags=["Categories"],
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_category(
    id: int, current_user: User = Depends(get_current_active_user)
):
    """Remove one of the category in the database.

    Args:
        id (int): Key to search category in the database.
        current_user (User, optional):  logged in user token. Defaults to Depends(get_current_active_user).

    Returns:
          N/A: --
    """
    session.execute(categories.delete().where(categories.c.category_id == id))
    session.commit()
    return session.execute(
        categories.select().where(categories.c.category_id == id)
    ).first()
