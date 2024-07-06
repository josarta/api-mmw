from typing import List
from fastapi import APIRouter, status
from sqlalchemy import func 
from config.db import session
from models.category import categories 
from schemas.category import Category , CategoryCount


category = APIRouter();



@category.get("/categories", 
   tags=["Categories"],
    response_model=List[Category],
    description="Get a list of all categories",)
async def get_all_categories():
     return session.query(categories).all();


@category.get("/categories/count", 
              tags=["Categories"], 
              description="Return count of avaliable categories",
              response_model=CategoryCount)
async def get_categories_count():
    result = session.query(func.count(categories.c.category_id)).scalar()
    return {"total": result}


@category.post("/categories", 
   tags=["Categories"],
    response_model=Category,
    description="Add new category.",)
async def create_new_categories(category:Category):
     new_category = {"name": category.name}
     result = session.execute(categories.insert().values(new_category))
     session.commit()
     return session.execute(categories.select().where(categories.c.category_id == result.lastrowid)).first()


@category.get(
    "/categories/{id}",
    tags=["Categories"],
     response_model=Category,
     description="Get a single tion by id.")
async def get_category(id: str):
     return session.execute(categories.select().where(categories.c.category_id == id)).first()

@category.put(
    "/categories/{id}",  tags=["Categories"], response_model=Category, description="Update a category by Id")
async def update_category(category:Category, id: int):
    session.execute(
        categories.update()
        .values(name = category.name)
        .where(categories.c.category_id== id)
    )
    session.commit()
    return session.execute(categories.select().where(categories.c.category_id == id)).first()

@category.delete("/categories/{id}", tags=["Categories"], status_code= status.HTTP_204_NO_CONTENT)
def delete_category(id: int):
    session.execute(categories.delete().where(categories.c.category_id == id))
    session.commit()
    return session.execute(categories.select().where(categories.c.category_id == id)).first()

