from pydantic import BaseModel
from src.models.token import Tokens
from src.models.users import UserRead
from typing import Optional


class UserAndTokens(BaseModel):
    User: Optional[UserRead]
    Token: Optional[Tokens]

    class Config:
        orm_mode = True
