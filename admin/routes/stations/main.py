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


@router.get("/", name="stations")
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
    return templates.TemplateResponse("pages/stations/list.html", context)


@router.get("/{station_id}", name="station_detail")
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
    return templates.TemplateResponse("pages/stations/detail.html", context)


@router.post("/{station_id}/edit/", name='station_edit')
async def admin_station_edit(request: Request, station_id: int, repo: Annotated[RequestsRepo, Depends(get_repo)]):
    print('method', request.method)
    form_data = await request.form()
    data = dict(form_data.items())

    for key, value in data.items():
        if key.startswith('has'):
            data[key] = True if value == 'Да' else False
    await repo.places.update_place(place_id=station_id, **data)
    redirect_url = request.url_for('station_detail', station_id=station_id)
    return RedirectResponse(url=redirect_url, status_code=302)


@router.get('/{station_id}/comments/{comment_id}/', name='delete_comment')
async def delete_comment(
        request: Request, station_id: int, comment_id: int,
        repo: Annotated[RequestsRepo, Depends(get_repo)]
):
    await repo.place_comments.delete_comment(comment_id=comment_id)
    redirect_url = request.url_for('station_detail', station_id=station_id)
    return RedirectResponse(redirect_url)
