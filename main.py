from fastapi import FastAPI , Request
from core.config import settings
from routes.location import location
from routes.category import category
from routes.audit import audit
from routes.token import token
from config.cors import init_cors
from middlewares.exception import ExceptionHandlerMiddleware

app = FastAPI(title=settings.PROJECT_NAME,version=settings.PROJECT_VERSION, swagger_ui_parameters={"syntaxHighlight.theme": "obsidian"})

init_cors(app)
app.include_router(location)
app.include_router(category)
app.include_router(audit)
app.include_router(token)
app.add_middleware(ExceptionHandlerMiddleware)
