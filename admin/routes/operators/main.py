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


@router.get("/operators/", name="operators")
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


@router.get("/operators/{operator_id}", name="operator_detail")
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
