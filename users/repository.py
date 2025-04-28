from datetime import datetime
from typing import List

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from roles.exceptions import RoleNotFound
from security.authorization import get_password_hash, verify_password
from users.exceptions import (
    IncorrectUserPassword,
    UserAlreadyExists,
    UserIsBanned,
    UserNotFound,
)
from users.models import UserCreate, UserDB, UserDeleted, UserRead, UserUpdate


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all_users(self) -> List[UserRead]:
        result = await self.db.execute(select(UserDB))
        users_db = result.scalars().all()
        return [UserRead.model_validate(user) for user in users_db]

    async def _get_user_by_id(self, user_id: int) -> UserDB:
        result = await self.db.execute(select(UserDB).where(UserDB.id == user_id))
        user_db = result.scalar_one_or_none()
        if user_db is None:
            raise UserNotFound()
        return user_db

    async def get_user_by_username(self, username: str) -> UserDB:
        result = await self.db.execute(
            select(UserDB).where(UserDB.username == username)
        )
        user_db = result.scalar_one_or_none()
        if user_db is None:
            raise UserNotFound()
        return user_db

    async def get_user(self, user_id: int) -> UserRead:
        user_db = await self._get_user_by_id(user_id)
        return UserRead.model_validate(user_db)

    async def create_user(self, user: UserCreate) -> UserRead:
        user_db = UserDB(
            username=user.username,
            password=get_password_hash(user.password),
            description=user.description,
            last_active=datetime.now(),
        )
        self.db.add(user_db)
        try:
            await self.db.commit()
            await self.db.refresh(user_db)
        except IntegrityError:
            await self.db.rollback()
            raise UserAlreadyExists()
        return UserRead.model_validate(user_db)

    async def update_user(self, user_id: int, user: UserUpdate) -> UserRead:
        user_db = await self._get_user_by_id(user_id)
        user_db.username = user.username
        user_db.description = user.description
        await self.db.commit()
        await self.db.refresh(user_db)
        return UserRead.model_validate(user_db)

    async def edit_user_role(self, user_id: int, role: str) -> UserRead:
        user_db = await self._get_user_by_id(user_id)
        user_db.role = role
        try:
            await self.db.commit()
            await self.db.refresh(user_db)
        except IntegrityError:
            await self.db.rollback()
            raise RoleNotFound()
        return UserRead.model_validate(user_db)

    async def delete_user(self, user_id: int) -> UserDeleted:
        user_db = await self._get_user_by_id(user_id)
        await self.db.delete(user_db)
        await self.db.commit()
        return UserDeleted.model_validate(user_db)

    async def authenticate_user(self, username: str, password: str) -> UserDB:
        user = await self.get_user_by_username(username)
        if not user or not verify_password(password, user.password):
            raise IncorrectUserPassword()
        if not user.is_active:
            raise UserIsBanned()
        return user
