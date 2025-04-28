from typing import List

from fastapi import APIRouter

from roles.dependencies import (
    DeleteUserPermission,
    ReadUserPermission,
    UpdateUserPermission,
)
from security.dependencies import OAuth
from users.dependencies import CurrentUserDB, UserRepo
from users.models import UserCreate, UserDeleted, UserRead, UserUpdate

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/")
async def get_all_users(
    user_repo: UserRepo, permission: ReadUserPermission
) -> List[UserRead]:
    return await user_repo.get_all_users()


@router.get("/me")
async def get_user_me(currect_user_db: CurrentUserDB) -> UserRead:
    return UserRead.model_validate(currect_user_db)


@router.get("/{id}")
async def get_user(
    id: int, user_repo: UserRepo, oauth: OAuth, permission: ReadUserPermission
) -> UserRead:
    return await user_repo.get_user(id)


@router.post("/")
async def create_user(user: UserCreate, user_repo: UserRepo) -> UserRead:
    return await user_repo.create_user(user)


@router.put("/me")
async def update_user_me(
    user: UserUpdate, currect_user_db: CurrentUserDB, user_repo: UserRepo
) -> UserRead:
    return await user_repo.update_user(currect_user_db.id, user)


@router.put("/{id}")
async def update_user(
    id: int, user: UserUpdate, user_repo: UserRepo, permission: UpdateUserPermission
) -> UserRead:
    return await user_repo.update_user(id, user)


@router.patch("/{id}/role")
async def edit_user_role(
    id: int, role: str, user_repo: UserRepo, permission: UpdateUserPermission
) -> UserRead:
    return await user_repo.edit_user_role(id, role)


@router.delete("/me")
async def delete_user_me(
    currect_user_db: CurrentUserDB, user_repo: UserRepo
) -> UserDeleted:
    return await user_repo.delete_user(currect_user_db.id)


@router.delete("/{id}")
async def delete_user(
    id: int, user_repo: UserRepo, permission: DeleteUserPermission
) -> UserDeleted:
    return await user_repo.delete_user(id)
