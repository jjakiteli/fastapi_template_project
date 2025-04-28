import os
from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import Depends
from jwt.exceptions import InvalidTokenError

from security.authorization import oauth2_scheme
from security.exceptions import InvalidCredentials
from security.models import TokenData

OAuth = Annotated[str, Depends(oauth2_scheme)]

ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")


async def get_current_user_username(token: OAuth):
    credentials_exception = InvalidCredentials()
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        print(username)
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    return token_data.username


CurrentUsername = Annotated[str, Depends(get_current_user_username)]


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
