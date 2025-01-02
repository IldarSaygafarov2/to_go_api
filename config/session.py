import string
from dataclasses import dataclass


@dataclass
class SessionConfig:
    max_age: int = 3600

    @property
    def session_choices(self):
        return string.ascii_letters + string.digits + '=+%$#'
