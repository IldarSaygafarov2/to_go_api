from dataclasses import dataclass
from typing import Optional

from environs import Env


@dataclass
class RedisConfig:
    redis_pass: Optional[str]
    redis_port: int
    redis_host: str

    def dsn(self) -> str:
        if self.redis_pass:
            return f"redis://:{self.redis_pass}@{self.redis_host}:{self.redis_port}/0"
        return f"redis://:{self.redis_host}:{self.redis_port}/0"

    @staticmethod
    def from_env(env: Env) -> "RedisConfig":
        return RedisConfig(
            redis_pass=env.str("REDIS_PASSWORD", None),
            redis_port=env.int("REDIS_PORT"),
            redis_host=env.str("REDIS_HOST"),
        )
