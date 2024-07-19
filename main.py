from fastapi import FastAPI , Request 
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from core.config import settings
from routes.location import location
from routes.category import category
from routes.audit import audit
from routes.token import token
from routes.location_category import locationCategoryReviewed
from config.cors import init_cors
from middlewares.exception import ExceptionHandlerMiddleware
from fastapi.templating import Jinja2Templates


app = FastAPI(title=settings.PROJECT_NAME,version=settings.PROJECT_VERSION, swagger_ui_parameters={"syntaxHighlight.theme": "obsidian"})


init_cors(app)
app.include_router(location)
app.include_router(category)
app.include_router(audit)
app.include_router(token)
app.include_router(locationCategoryReviewed)
app.add_middleware(ExceptionHandlerMiddleware)

templates = Jinja2Templates(directory="templates")
app.mount("/templates", StaticFiles(directory="templates"), name="static")


def generate_html_response(request: Request):
    html_content =  templates.TemplateResponse(
        request=request, name="404.html", context={}
    )
    return html_content


@app.get("/", response_class=HTMLResponse)
async def read_default(request: Request):
    return generate_html_response(request)
