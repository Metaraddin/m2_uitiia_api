from datetime import datetime
from pydantic import BaseModel, constr


class NewsInput(BaseModel):
    title: constr(max_length=100)
    content: constr(max_length=5000)


class NewsRead(BaseModel):
    id: int
    datetime: datetime

    class Config:
        orm_mode = True
