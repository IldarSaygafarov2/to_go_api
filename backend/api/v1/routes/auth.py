from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from backend.app.config import config
from backend.app.dependencies import get_jwt_service, get_repo, get_sms_service
from backend.core.interactors.login_user import LoginUserInteractor
from backend.core.interfaces.user import UserAuthDTO, UserRegistrationDTO
from backend.core.services.jwt_service import JwtService
from backend.core.services.sms_service import SMSService
from infrastructure.database.repo.requests import RequestsRepo
from infrastructure.utils.helpers import generate_code
from messages.auth import SMS_MESSAGE

router = APIRouter(
    prefix=config.api_prefix.v1.auth,
    tags=["Auth"],
)


@router.post("/login")
async def login(
    user_data: UserAuthDTO,
    repo: Annotated[RequestsRepo, Depends(get_repo)],
    jwt_service: Annotated[JwtService, Depends(get_jwt_service)],
):
    verification_code = await repo.users_verification.is_code_exists(
        phone_number=user_data.phone_number,
        code=user_data.code,
    )
    if verification_code is None:
        return {"message": "Введеный код неверный", "is_verified": False}

    interactor = LoginUserInteractor(
        request_repo=repo,
        jwt_service=jwt_service,
    )
    try:
        token = await interactor(user_data)
        return {"access_token": token, "token_type": "bearer"}
    except ValueError as e:
        return JSONResponse(content={"UNAUTHORIZED": str(e)}, status_code=401)


@router.post("/code/send")
async def send_code(
    user_data: UserRegistrationDTO,
    sms_service: Annotated[SMSService, Depends(get_sms_service)],
    repo: Annotated[RequestsRepo, Depends(get_repo)],
):
    verification_code = generate_code()

    new_verified = await repo.users_verification.insert_verification_code(
        phone_number=user_data.phone_number,
        code=verification_code,
    )

    sms_service.send_message(
        phone_number=user_data.phone_number,
        message=SMS_MESSAGE.format(code=verification_code),
    )

    return UserAuthDTO.model_validate(new_verified, from_attributes=True)


@router.post("/registration")
async def verify_code(
    user_data: UserAuthDTO,
    repo: Annotated[RequestsRepo, Depends(get_repo)],
):
    user_verification_code = await repo.users_verification.is_code_exists(
        phone_number=user_data.phone_number,
        code=user_data.code,
    )

    if user_verification_code is None:
        return {"message": "Введен неверный код", "is_verified": False}

    await repo.users.insert_user(phone_number=user_data.phone_number)
    return {"message": "Регистрация прошла успешно", "is_verified": True}


# 998900375350
# 7456
