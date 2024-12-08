from typing import Annotated, Optional

from fastapi import APIRouter, Body, Depends, File, UploadFile

from backend.app.config import config
from backend.app.dependencies import get_repo
from backend.core.interfaces.user import UserProfileDTO, UserProfileUpdateDTO
from infrastructure.database.repo.requests import RequestsRepo
from infrastructure.utils.helpers import create_user_profile_dir

router = APIRouter(
    prefix=config.api_prefix.v1.users,
    tags=["Users"],
)


@router.get("/{user_id}/profile")
async def get_user_profile(
    user_id: int,
    repo: Annotated[RequestsRepo, Depends(get_repo)],
) -> UserProfileDTO:
    profile = await repo.users.get_user_by_id(user_id=user_id)
    return UserProfileDTO.model_validate(profile, from_attributes=True)


@router.patch("/{user_id}/profile/update/")
async def update_user_profile(
    user_id: int,
    repo: Annotated[RequestsRepo, Depends(get_repo)],
    fullname: str = Body(...),
    user_photo: Optional[UploadFile] = File(None),
) -> UserProfileDTO:
    _dir = create_user_profile_dir(user_id)

    file_name = user_photo.filename
    path = _dir / file_name
    with open(path, "wb") as file:
        file.write(await user_photo.read())

    user_profile = await repo.users.update_user(
        user_id=user_id,
        fullname=fullname,
        user_photo=str(path),
    )
    return UserProfileDTO.model_validate(user_profile, from_attributes=True)
