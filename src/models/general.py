from pydantic import BaseModel
from models.token import Tokens
from models.users import UserRead
from typing import Optional


class UserAndTokens(BaseModel):
    User: Optional[UserRead]
    Token: Optional[Tokens]

    class Config:
        orm_mode = True
