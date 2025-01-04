import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from admin.routes.auth.main import router as auth_router
from backend.app.dependencies import get_repo
from infrastructure.database.repo.requests import RequestsRepo

templates = Jinja2Templates(directory="templates")

admin_router = APIRouter(prefix="/admin")
admin_router.include_router(auth_router)

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


@admin_router.get("/operators/", name="operators")
async def admin_operators(
    request: Request, repo: Annotated[RequestsRepo, Depends(get_repo)]
):
    if not request.user.is_authenticated:
        return RedirectResponse(url=auth_login_url)
    operators = await repo.operators.get_all_operators()
    context = {
        "request": request,
        "operators": enumerate(operators, start=1),
    }
    return templates.TemplateResponse("pages/operators_list.html", context)


@admin_router.get("/operators/{operator_id}", name="operator_detail")
async def admin_operator_detail(
    request: Request, operator_id: int, repo: Annotated[RequestsRepo, Depends(get_repo)]
):
    if not request.user.is_authenticated:
        return RedirectResponse(url=auth_login_url)
    operator = await repo.operators.get_operator_by_id(operator_id)
    context = {
        "request": request,
        "operator": operator,
    }
    return templates.TemplateResponse("pages/operator_detail.html", context)


# @admin_router.get('/stations/', name='stations')
@admin_router.get("/stations/", name="stations")
async def admin_all_stations(
    request: Request, repo: Annotated[RequestsRepo, Depends(get_repo)], page: int = 1
):
    if not request.user.is_authenticated:
        return RedirectResponse(url=auth_login_url)
    limit = 14
    stations = await repo.places.get_places(limit=limit, offset=page)
    total_places = await repo.places.count_total_places()
    context = {
        "request": request,
        "stations": stations,
        "total_places": total_places,
        "page": page,
    }
    return templates.TemplateResponse("pages/stations.html", context)


@admin_router.get("/stations/{station_id}", name="station_detail")
async def admin_station_detail(
    request: Request, station_id: int, repo: Annotated[RequestsRepo, Depends(get_repo)]
):
    if not request.user.is_authenticated:
        return RedirectResponse(url=auth_login_url)
    station, _ = await repo.places.get_place(place_id=station_id)

    context = {
        "request": request,
        "station": station,
    }
    return templates.TemplateResponse("pages/station_detail.html", context)
