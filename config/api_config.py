from dataclasses import dataclass, field

from environs import Env


@dataclass
class RunConfig:
    api_host: str
    api_port: int

    @staticmethod
    def from_env(env: Env) -> "RunConfig":
        return RunConfig(
            api_host=env.str("API_HOST"),
            api_port=env.int("API_PORT"),
        )


@dataclass
class ApiV1Prefix:
    prefix: str = "/v1"
    auth: str = "/auth"
    places: str = "/places"
    users: str = "/users"
    pages: str = "/pages"


@dataclass
class ApiPrefix:
    prefix: str = "/api"
    v1: ApiV1Prefix = field(default_factory=ApiV1Prefix)


@dataclass
class AccessTokenConfig:
    token_secret: str
    algorith: str = "HS256"
    token_expire_seconds: int = 86400

    @staticmethod
    def from_env(env: Env):
        return AccessTokenConfig(
            token_secret=env.str("SECRET_KEY"),
        )
