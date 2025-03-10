from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from backend.app.config import config


router = APIRouter(
    prefix=config.api_prefix.v1.pages,
    tags=["Pages"],
)
templates = Jinja2Templates(directory="templates")


@router.get("/")
async def get_pages_html(request: Request):
    context = {
        "request": request,
    }
    return templates.TemplateResponse(name="chat.html", context=context)


@router.get("/private")
async def get_pages_html(request: Request):
    context = {
        "request": request,
    }
    return templates.TemplateResponse(name="private_chat.html", context=context)


@router.get("/support")
async def get_support_page_html(request: Request):
    context = {
        "request": request,
    }
    return templates.TemplateResponse(name="support_chat.html", context=context)
