from datetime import datetime
from pydantic import BaseModel, constr


class NewsInput(BaseModel):
    title: constr(max_length=100)
    content: constr(max_length=5000)


class NewsRead(BaseModel):
    id: int
    datetime: datetime
    title: str
    content: str
    user: str

    class Config:
        orm_mode = True
