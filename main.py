from fastapi import FastAPI , Request
from core.config import settings
from routes.location import location
from routes.category import category
from routes.audit import audit

from middlewares.exception import ExceptionHandlerMiddleware

app = FastAPI(title=settings.PROJECT_NAME,version=settings.PROJECT_VERSION)
app.include_router(location)
app.include_router(category)
app.include_router(audit)
app.add_middleware(ExceptionHandlerMiddleware)
