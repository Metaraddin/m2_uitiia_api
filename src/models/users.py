from pydantic import BaseModel, EmailStr, constr


class UserBase(BaseModel):
    id: int
    email: EmailStr
    first_name: constr(min_length=1, max_length=30)
    last_name: constr(min_length=1, max_length=30)
    middle_name: constr(min_length=1, max_length=30)


class UserRead(BaseModel):
    id: int
    email: EmailStr
    first_name: constr(min_length=1, max_length=30)
    last_name: constr(min_length=1, max_length=30)
    middle_name: constr(min_length=1, max_length=30)

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
