from pydantic import BaseModel, EmailStr, constr
from typing import Optional


class UserBase(BaseModel):
    id: int
    email: EmailStr
    first_name: constr(min_length=1, max_length=30)
    last_name: constr(min_length=1, max_length=30)
    middle_name: constr(min_length=1, max_length=30)
    hashed_password = str
    avatar_uri: Optional[str]


class UserRead(BaseModel):
    id: int
    email: EmailStr
    first_name: constr(min_length=1, max_length=30)
    last_name: constr(min_length=1, max_length=30)
    middle_name: constr(min_length=1, max_length=30)
    avatar_uri: Optional[str]

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    email: EmailStr
    password: constr(min_length=6, max_length=30)
    first_name: constr(min_length=1, max_length=30)
    last_name: constr(min_length=1, max_length=30)
    middle_name: constr(min_length=1, max_length=30)


class UserLogin(BaseModel):
    email: EmailStr
    password: constr(min_length=6, max_length=30)
    remember_me: bool


class UserAvatarUpdate(BaseModel):
    avatar_uri: str
