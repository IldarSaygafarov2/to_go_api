from typing import Annotated

from fastapi import APIRouter, Depends

from backend.app.config import config
from backend.app.dependencies import get_repo
from backend.core.interfaces.operator import (
    OperatorCreateDTO,
    OperatorDTO,
    OperatorEditDTO,
)
from infrastructure.database.repo.requests import RequestsRepo

router = APIRouter(
    prefix=config.api_prefix.v1.operators,
    tags=["Support Operators"],
)


@router.get("/", response_model=list[OperatorDTO])
async def get_all_operators(
    repo: Annotated[RequestsRepo, Depends(get_repo)],
):
    operators = await repo.operators.get_all_operators()
    return operators


@router.get("/{operator_id}", response_model=OperatorDTO)
async def get_operator_detail(
    operator_id: int,
    repo: Annotated[RequestsRepo, Depends(get_repo)],
):
    operator = await repo.operators.get_operator_by_id(operator_id=operator_id)
    return operator


@router.post("/add", response_model=OperatorDTO)
async def add_new_operator(
    operator_data: OperatorCreateDTO,
    repo: Annotated[RequestsRepo, Depends(get_repo)],
):
    new_operator = await repo.operators.add_operator(
        fullname=operator_data.fullname,
        telegram_username=operator_data.telegram_username,
    )
    return OperatorDTO.model_validate(new_operator, from_attributes=True)


@router.patch("/{operator_id}/edit")
async def edit_operator_data(
    operator_id: int,
    operator_data: dict,
    repo: Annotated[RequestsRepo, Depends(get_repo)],
):
    pass


@router.delete("/{operator_id}")
async def delete_operator(
    operator_id: int,
    repo: Annotated[RequestsRepo, Depends(get_repo)],
):
    pass
