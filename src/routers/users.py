from typing import List

from fastapi import APIRouter, Depends, HTTPException
from fastapi_jwt_auth import AuthJWT
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session

from src.app.dependencies import get_db
from src.models.users import UserRead, UserCreate, UserLogin
from src.models.general import UserAndTokens
from src.repositories import users


router = APIRouter(prefix="/user", tags=["User"])
security = HTTPBearer()


@router.post("/", status_code=200, response_model=UserAndTokens)
async def create_user(user_info: UserCreate, session: Session = Depends(get_db),
                      Authorize: AuthJWT = Depends()):
    """
    Создаёт нового пользователя и возвращает его вместе с access token.
    """
    curr_user = users.create_user(u=user_info, s=session)
    if not curr_user:
        raise HTTPException(status_code=400, detail=[{'msg': 'User with this email already exists'}])
    token = users.create_user_token(curr_user.id, Authorize)
    return UserAndTokens(User=curr_user, Token=token)


@router.post("/login", status_code=200, response_model=UserAndTokens)
async def login(user_info: UserLogin, session: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    """
    Проверяет email и пароль.
    Если remember=True записывает access и refrest токены в куки и возвращает их.
    Иначе записывает и возвращает только access токен.
    Так же возвращает пользователя.
    """
    curr_user = users.get_user_by_email(email=user_info.email, s=session)
    if not curr_user:
        raise HTTPException(status_code=400, detail=[{'msg': 'User with this email does not exist'}])
    if not users.validate_password(password=user_info.password, hashed_password=curr_user.hashed_password):
        raise HTTPException(status_code=400, detail=[{'msg': 'Incorrect email or password'}])
    token = users.create_user_token(id=curr_user.id, remember=user_info.remember_me, Authorize=Authorize)
    return UserAndTokens(
        User=curr_user,
        Token=token
    )


@router.get("/refresh", status_code=200, response_model=UserAndTokens)
async def refresh(session: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    """
    Обновляет access токен
    """
    Authorize.jwt_refresh_token_required()

    curr_user = users.get_user_by_id(int(Authorize.get_jwt_subject()), session)
    if not curr_user:
        raise HTTPException(status_code=400)

    token = users.create_user_token(id=curr_user.id, Authorize=Authorize, remember=False)
    return UserAndTokens(
        User=curr_user,
        Token=token
    )


@router.delete('/login', status_code=200)
async def logout(Authorize: AuthJWT = Depends()):
    """
    Выход из аккаунта
    """
    Authorize.jwt_required()
    Authorize.unset_jwt_cookies()
    return {'mgs': 'Successfully logout'}


@router.get("/all", status_code=200, response_model=List[UserRead])
async def get_all_user(limit: int = 100, skip: int = 0, session: Session = Depends(get_db)):
    """
    Возвращает список всех пользователей.
    """
    return users.get_all_user(session, limit, skip)


@router.get("/curr", status_code=200, response_model=UserRead)
async def get_current_user(session: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    """
    Возвращает авторизованного пользователя.
    """
    Authorize.jwt_required()
    curr_user = users.get_user_by_id(int(Authorize.get_jwt_subject()), session)
    if not curr_user:
        raise HTTPException(status_code=400, detail=[{'msg': 'User with this email does not exist'}])
    return curr_user


@router.get("/{id}", status_code=200, response_model=UserRead)
async def get_user(id: int, session: Session = Depends(get_db)):
    """
    Возвращает пользователя по **user.id**
    """
    curr_user = users.get_user_by_id(id, session)
    if not curr_user:
        raise HTTPException(status_code=400, detail=[{'msg': 'User with this id does not exist'}])
    return