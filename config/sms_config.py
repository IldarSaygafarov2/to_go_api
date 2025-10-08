from dataclasses import dataclass

from environs import Env


@dataclass
class SMSConfig:
    auth_email: str
    auth_secret_key: str
    api_url: str
    main_phone_number: str
    main_code: str

    @staticmethod
    def from_env(env: Env) -> "SMSConfig":
        return SMSConfig(
            auth_email=env.str("SMS_AUTH_EMAIL"),
            auth_secret_key=env.str("SMS_AUTH_SECRET_KEY"),
            api_url=env.str("SMS_API_URL"),
            main_phone_number=env.str('MAIN_PHONE_NUMBER'),
            main_code=env.str('MAIN_CODE'),
        )
