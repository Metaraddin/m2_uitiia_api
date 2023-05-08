import random
import hashlib
import string

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.models.users import UserCreate
from app.models.token import Tokens
from app.database.users import User


def __hash_password(password: str, salt: str = None):
    if salt is None:
        salt = "".join(random.choice(string.ascii_letters) for _ in range(12))
    enc = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 100_000)
    return enc.hex()


def validate_password(password: str, hashed_password: str):
    salt, hashed = hashed_password.split("$")
    return __hash_password(password, salt) == hashed


def create_user_token(id: int, remember: bool, Authorize):
    access_token = Authorize.create_access_token(subject=id)
    Authorize.set_access_cookies(access_token)

    if remember:
        refresh_token = Authorize.create_refresh_token(subject=id)
        Authorize.set_refresh_cookies(refresh_token)
        return Tokens(access_token=access_token, refresh_token=refresh_token)
    else:
        return Tokens(access_token=access_token)


def create_user(u: UserCreate, s: Session):
    user = User()
    user.email = u.email
    salt = "".join(random.choice(string.ascii_letters) for _ in range(12))
    hashed_password = __hash_password(salt=salt, password=u.password)
    user.hashed_password = f"{salt}${hashed_password}"
    user.first_name = u.first_name
    user.last_name = u.last_name
    user.middle_name = u.middle_name

    s.add(user)
    try:
        s.commit()
        return user
    except IntegrityError:
        return None


def get_user_by_email(email: str, s: Session):
    return s.query(User).filter(User.email == email).first()


def get_user_by_id(id: int, s: Session):
    return s.query(User).filter(User.id == id).first()


def get_all_user(s: Session, limit: int = 100, skip: int = 0):
    return s.query(User).limit(limit).offset(skip).all()


def update_avatar_user(id: int, s: Session, avatar_uri: str = None):
    user = s.query(User).filter(User.id == id).first()
    if user:
        user.avatar_uri = avatar_uri
        s.add(user)
        s.commit()
        return user
