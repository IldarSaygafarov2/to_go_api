from environs import Env
from dataclasses import dataclass

from sqlalchemy.engine.url import URL


@dataclass
class DbConfig:
    host: str
    password: str
    user: str
    database: str
    port: int = 5432

    def construct_sqlalchemy_url(self, driver="asyncpg") -> str:
        return URL.create(
            drivername=f"postgresql+{driver}",
            username=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
            database=self.database,
        ).render_as_string(hide_password=False)

    @staticmethod
    def from_env(env: Env) -> "DbConfig":
        return DbConfig(
            host=env.str("DB_HOST"),
            password=env.str("POSTGRES_PASSWORD"),
            user=env.str("POSTGRES_USER"),
            database=env.str("POSTGRES_DB"),
            port=env.int("DB_PORT", 5432),
        )
