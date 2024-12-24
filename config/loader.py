from dataclasses import dataclass
from typing import Optional

from environs import Env

from config.api_config import AccessTokenConfig, ApiPrefix, RunConfig
from config.db_config import DbConfig
from config.sms_config import SMSConfig
from config.tg_config import TgConfig


@dataclass
class Config:
    db: DbConfig
    run_api: RunConfig
    api_prefix: ApiPrefix
    sms: SMSConfig
    access_token: AccessTokenConfig
    telegram: TgConfig


def load_config(path: Optional[str] = None) -> "Config":
    env = Env()
    env.read_env(path)

    db_config = DbConfig.from_env(env)
    run_api = RunConfig.from_env(env)
    sms = SMSConfig.from_env(env)
    access_token = AccessTokenConfig.from_env(env)
    telegram = TgConfig.from_env(env)
    api_prefix = ApiPrefix()

    return Config(
        db=db_config,
        run_api=run_api,
        api_prefix=api_prefix,
        sms=sms,
        access_token=access_token,
        telegram=telegram,
    )
