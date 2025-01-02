import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from backend.app.config import config
from backend.app.dependencies import get_repo
from backend.core.services.auth import AuthUser
from infrastructure.database.repo.requests import RequestsRepo

templates = Jinja2Templates(directory="templates")

admin_router = APIRouter(prefix="/admin")


@admin_router.get("/", name="admin")
async def show_admin_home_page(request: Request):
    # if not request.user.is_authenticated:
    #     return RedirectResponse(url="login/")
    return templates.TemplateResponse("pages/index.html", {"request": request})


@admin_router.get("/login/", name="login")
async def admin_login(request: Request):
    return templates.TemplateResponse("pages/login.html", {"request": request})


@admin_router.post("/login/", name="login")
async def admin_login(
    request: Request, repo: Annotated[RequestsRepo, Depends(get_repo)]
):
    form_data = await request.form()
    username = form_data.get("username")
    password = form_data.get("password")

    user = await repo.web_users.get_user_by_username_and_password(
        username=username, password=password
    )
    if user is None:
        return templates.TemplateResponse(
            "pages/login.html", {"request": request, "error": "User not found"}
        )

    expires = datetime.datetime.now() + datetime.timedelta(
        seconds=config.session.max_age
    )
    if await repo.auth_session.get_session_by_token(token=request.session):
        await repo.auth_session.delete_session(token=request.session)
    session = await repo.auth_session.create_session(
        user_id=user.id, token=request.session, expire_at=expires
    )
    request.scope["session"] = session.token
    request.scope["auth"] = user.scope
    auth_user = AuthUser(session, repo)
    auth_user.__user = user
    request.scope["user"] = auth_user
    
    

    return RedirectResponse('admin')


@admin_router.get("/profile/", name="profile")
async def admin_profile(request: Request):
    return templates.TemplateResponse("pages/profile.html", {"request": request})


@admin_router.get("/operators/", name="operators")
async def admin_operators(
    request: Request, repo: Annotated[RequestsRepo, Depends(get_repo)]
):
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
    station, _ = await repo.places.get_place(place_id=station_id)

    context = {
        "request": request,
        "station": station,
    }
    return templates.TemplateResponse("pages/station_detail.html", context)
