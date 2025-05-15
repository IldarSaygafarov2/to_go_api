from dataclasses import dataclass
from environs import Env


@dataclass
class GmailConfig:

    mail_username: str
    mail_password: str
    mail_from: str
    mail_port: int
    mail_server: str
    mail_from_name: str

    @staticmethod
    def from_env(env: Env):
        return GmailConfig(
            mail_username=env.str("MAIL_USERNAME"),
            mail_password=env.str("MAIL_PASSWORD"),
            mail_from=env.str("MAIL_FROM"),
            mail_port=env.int("MAIL_PORT"),
            mail_server=env.str("MAIL_SERVER"),
            mail_from_name=env.str("MAIL_FROM_NAME"),
        )
