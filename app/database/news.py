from datetime import datetime
from sqlalchemy import Column, Integer, DateTime, String

from app.database.database import DataBase


class News(DataBase):
    __tablename__ = 'news'
    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    datetime = Column(DateTime, default=datetime.utcnow, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    user = Column(String, nullable=False)
