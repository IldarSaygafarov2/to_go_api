import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from admin.routes.auth.main import router as auth_router
from admin.routes.operators.main import router as operators_router
from admin.routes.stations.main import router as stations_router
from backend.app.dependencies import get_repo
from infrastructure.database.repo.requests import RequestsRepo

templates = Jinja2Templates(directory="templates")

admin_router = APIRouter(prefix="/admin")
admin_router.include_router(auth_router)
admin_router.include_router(stations_router)
admin_router.include_router(operators_router)

auth_login_url = "/admin/auth/login/"


@admin_router.get("/", name="admin")
async def show_admin_home_page(request: Request):
    print("METHOD", request.method)
    if not request.user.is_authenticated:
        return RedirectResponse(url=auth_login_url)

    return templates.TemplateResponse("pages/index.html", {"request": request})


@admin_router.get("/profile/", name="profile")
async def admin_profile(request: Request):
    if not request.user.is_authenticated:
        return RedirectResponse(url=auth_login_url)
    return templates.TemplateResponse("pages/profile.html", {"request": request})


@admin_router.get("/support/", name="support")
async def get_support_page(
    request: Request,
    repo: Annotated[RequestsRepo, Depends(get_repo)],
):
    operator_id = request.user.id
    operator = await repo.operators.get_operator_by_id(operator_id=operator_id)
    support_rooms = await repo.support_room.get_support_rooms(operator_id=operator_id)
    context = {
        "request": request,
        "rooms": support_rooms,
        "operator": operator,
    }
    return templates.TemplateResponse("pages/support.html", context)
