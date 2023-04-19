from pydantic import BaseModel
from typing import Optional


class Tokens(BaseModel):
    access_token: str
    refresh_token: Optional[str]
