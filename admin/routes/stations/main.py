from typing import Annotated

from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from backend.app.dependencies import get_repo
from infrastructure.database.repo.requests import RequestsRepo

templates = Jinja2Templates(directory="templates")

router = APIRouter(
    prefix="/stations",
)

auth_login_url = "/admin/auth/login/"


tabs_list = [
    {"name": "Общая информация", "href": "commonTab"},
    {"name": "Фотографии", "href": "photoTab"},
    {"name": "Тип топлива", "href": "fuelTab"},
    {"name": "Комментарии", "href": "commentTab"},
]


@router.get("/stations/", name="stations")
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


@router.get("/stations/{station_id}", name="station_detail")
async def admin_station_detail(
    request: Request, station_id: int, repo: Annotated[RequestsRepo, Depends(get_repo)]
):
    if not request.user.is_authenticated:
        return RedirectResponse(url=auth_login_url)
    station, _ = await repo.places.get_place(place_id=station_id)

    context = {
        "request": request,
        "station": station,
        "tabs_list": tabs_list,
    }
    return templates.TemplateResponse("pages/station_detail.html", context)


@router.post('/stations/{station_id}/edit/')
async def admin_station_edit(request: Request, form_data=Form(...)):
    return {}
