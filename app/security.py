from datetime import datetime, timedelta
from typing import Union

from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

from app.db import db_instance


# openssl사용하여 키 만들기: openssl rand -hex 32
SECRET_KEY = "9186b13cdc10207c496feccc264e20fa4c433a1505138ee920eb9e291a40d863"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pws_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pws_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pws_context.hash(password)


def authenticate_user(username: str, password: str):
    user = db_instance.get_user(username)
    if user == None:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    
    return user


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt