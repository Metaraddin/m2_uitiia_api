from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from src.db.database import DataBase


class User(DataBase):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    middle_name = Column(String, nullable=True)
    hashed_password = Column(String, nullable=False)
