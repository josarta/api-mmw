from fastapi import FastAPI
from core.config import settings
from typing import Union

app = FastAPI(title=settings.PROJECT_NAME,version=settings.PROJECT_VERSION)


@app.get("/")
def read_root():
    return {"message": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}