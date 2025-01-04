from infrastructure.database.models import Session, User
from infrastructure.database.repo.requests import RequestsRepo
from infrastructure.database.setup import create_engine, create_session_pool
from backend.app.config import config


class BaseUser:
    @property
    def is_authenticated(self) -> bool:
        raise NotImplementedError()


class UnauthenticatedUser(BaseUser):
    @property
    def is_authenticated(self) -> bool:
        return False


class AuthUser(BaseUser):
    def __init__(self, session: Session, repo: RequestsRepo) -> None:
        self.session = session
        self.repo = repo
        self.__user = None

    @property
    def is_authenticated(self) -> bool:
        return True

    async def user(self) -> User:
        if not self.__user:
            self.__user = await self.repo.web_users.get_user(
                user_id=self.session.user_id
            )
        return self.__user
