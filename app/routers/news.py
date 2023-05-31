from typing import List

from fastapi import APIRouter, Depends, HTTPException
from fastapi_jwt_auth import AuthJWT
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.models.news import NewsInput, NewsRead
from app.repositories import news, users
from app.telegram_bot import post_news


router = APIRouter(prefix="/news", tags=["News"])
security = HTTPBearer()


@router.post("/", status_code=200, response_model=NewsRead)
async def create_news(news_info: NewsInput, session: Session = Depends(get_db),
                      Authorize: AuthJWT = Depends()):
    """
    Создаёт новый пост
    """
    Authorize.jwt_optional()

    if Authorize.get_jwt_subject():
        curr_user = users.get_user_by_id(int(Authorize.get_jwt_subject()), session)
        if not curr_user:
            raise HTTPException(status_code=400, detail=[{'msg': 'User does not exist'}])
    else:
        curr_user = None

    return news.create_news(n=news_info, s=session, u=curr_user)


@router.get("/all", status_code=200, response_model=List[NewsRead])
async def get_all_news(limit: int = 100, skip: int = 0, session: Session = Depends(get_db)):
    """
    Возвращает список всех постов.
    """
    return news.get_all_news(session, limit, skip)


@router.delete("/delete/{post_id}")
async def delete_news(post_id: int, session: Session = Depends(get_db)):
    """
    Удаляет пост из базы данных.
    """
    return news.delete_news_from_db(post_id=post_id, s=session)
