from typing import Optional

from pydantic import BaseModel


class GmailMessageSchema(BaseModel):
    name: Optional[str]
    email: Optional[str]
    subject: Optional[str]
    message: Optional[str]
