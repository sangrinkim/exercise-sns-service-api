from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.models.users import TokenData, User
from .security import *


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="사용자 인증에 실패했습니다.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    
    user = db_instance.get_user(token_data.username)
    if user is None:
        raise credentials_exception
    
    return user


async def get_current_user_permission(
    current_user: Annotated[User, Depends(get_current_user)]
):
    # Todo enum으로 처리..
    if current_user.permission == "user":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="접근 권한이 없습니다.")
    return current_user