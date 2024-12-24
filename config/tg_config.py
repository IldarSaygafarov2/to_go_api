from dataclasses import dataclass
from environs import Env


@dataclass
class TgConfig:
    token: str

    @staticmethod
    def from_env(env: Env) -> "TgConfig":
        return TgConfig(token=env.str("BOT_TOKEN"))
