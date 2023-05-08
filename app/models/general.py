from typing import Optional
from pydantic import BaseModel

from app.models.token import Tokens
from app.models.users import UserRead


class UserAndTokens(BaseModel):
    User: Optional[UserRead]
    Token: Optional[Tokens]

    class Config:
        orm_mode = True
