from datetime import datetime
from sqlalchemy import Column, Integer, DateTime

from app.database.database import DataBase


class News(DataBase):
    __tablename__ = 'news'
    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    datetime = Column(DateTime, default=datetime.utcnow, nullable=False)
