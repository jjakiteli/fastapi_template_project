from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from security.dependencies import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token
from security.models import Token
from users.dependencies import UserRepo

router = APIRouter(prefix="/login", tags=["Login"])


@router.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], user_repo: UserRepo
) -> Token:
    user = await user_repo.authenticate_user(form_data.username, form_data.password)
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")
