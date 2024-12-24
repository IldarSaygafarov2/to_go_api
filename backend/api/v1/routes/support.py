from typing import Annotated

from fastapi import APIRouter, Depends

from backend.app.config import config
from backend.app.dependencies import get_repo
from infrastructure.database.repo.requests import RequestsRepo

router = APIRouter(
    prefix=config.api_prefix.v1.support,
    tags=["Support"],
)


@router.post("{user_id}/send_message")
async def send_user_message_to_operators(
    user_id: int,
    message: str,
    repo: Annotated[RequestsRepo, Depends(get_repo)],
):
    operators = await repo.operators.get_all_operators()
    print(operators, message)
