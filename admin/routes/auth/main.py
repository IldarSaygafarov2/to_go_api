import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse, Response
from fastapi.templating import Jinja2Templates

from backend.app.config import config
from backend.app.dependencies import get_repo
from backend.core.services.auth import AuthUser
from infrastructure.database.repo.requests import RequestsRepo

templates = Jinja2Templates(directory="templates")


router = APIRouter(
    prefix="/auth",
)


@router.get("/login/", name="login")
async def admin_login(request: Request):
    if request.user.is_authenticated:
        return RedirectResponse("/admin/")
    return templates.TemplateResponse("pages/login.html", {"request": request})


@router.post("/login/", name="login")
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
    return templates.TemplateResponse("pages/index.html", {"request": request})


@router.get("/logout/", name="logout")
async def admin_logout(
    request: Request,
    repo: Annotated[RequestsRepo, Depends(get_repo)],
):
    token = request.cookies.get("session")
    await repo.auth_session.delete_session(token=token)
    request.cookies["session"] = None
    return RedirectResponse("/admin/")
