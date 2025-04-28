from typing import Annotated

from fastapi import Depends

from database.dependencies import DatabaseSession
from security.dependencies import CurrentUsername
from users.exceptions import UserIsBanned
from users.models import UserDB
from users.repository import UserRepository


async def get_user_repo(db: DatabaseSession) -> UserRepository:
    return UserRepository(db)


UserRepo = Annotated[UserRepository, Depends(get_user_repo)]


async def get_current_user(
    current_username: CurrentUsername, user_repo: UserRepo
) -> UserDB:
    user_db = await user_repo.get_user_by_username(current_username)
    if not user_db.is_active:
        raise UserIsBanned()
    return user_db


CurrentUserDB = Annotated[UserDB, Depends(get_current_user)]
