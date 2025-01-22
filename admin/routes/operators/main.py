from typing import Annotated

from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from backend.app.dependencies import get_repo
from infrastructure.database.repo.requests import RequestsRepo

router = APIRouter(
    prefix="/operators",
)

templates = Jinja2Templates(directory="templates")
auth_login_url = "/admin/auth/login/"


@router.get("/", name="operators")
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
    return templates.TemplateResponse("pages/operators/list.html", context)


@router.get("/{operator_id}", name="operator_detail")
async def admin_operator_detail(
    request: Request,
    operator_id: int,
    repo: Annotated[RequestsRepo, Depends(get_repo)],
):
    if not request.user.is_authenticated:
        return RedirectResponse(url=auth_login_url, status_code=302)
    operator = await repo.operators.get_operator_by_id(operator_id)
    context = {
        "request": request,
        "operator": operator,
    }

    return templates.TemplateResponse("pages/operators/detail.html", context)


@router.get("/create/", name="create_operator")
async def admin_operator_detail(
        request: Request,
        repo: Annotated[RequestsRepo, Depends(get_repo)],
):
    if not request.user.is_authenticated:
        return RedirectResponse(url=auth_login_url, status_code=302)

    context = {
        "request": request,
    }
    return templates.TemplateResponse("pages/operators/create.html", context)


@router.post("/create/", name="operator_create")
async def admin_operator_create(
        request: Request,
        repo: Annotated[RequestsRepo, Depends(get_repo)],
):
    data = await request.form()
    data = dict(data.items())

    new_operator = await repo.operators.add_operator(**data)
    redirect_url = request.url_for('operator_detail', operator_id=new_operator.id)
    return RedirectResponse(redirect_url, status_code=302)


@router.post('/{operator_id}/edit/', name='operator_update')
async def update_operator_data(request: Request, operator_id: int, repo: Annotated[RequestsRepo, Depends(get_repo)]):
    if not request.user.is_authenticated:
        return RedirectResponse(url=auth_login_url, status_code=302)

    data = await request.form()
    data = dict(data.items())
    data['telegram_chat_id'] = int(data['telegram_chat_id']) if data['telegram_chat_id'] else 0

    updated = await repo.operators.update_operator(operator_id=operator_id, **data)
    redirect_url = request.url_for('operator_detail', operator_id=operator_id)
    return RedirectResponse(url=redirect_url, status_code=302)
