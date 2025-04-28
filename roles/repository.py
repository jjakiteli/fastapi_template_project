from typing import List

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from roles.exceptions import RoleAlreadyExists, RoleNotFound
from roles.models import RoleCreate, RoleDB, RoleDeleted, RoleRead, RoleUpdate


class RoleRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all_roles(self) -> List[RoleRead]:
        result = await self.db.execute(select(RoleDB))
        roles_db = result.scalars().all()
        return [RoleRead.model_validate(role) for role in roles_db]

    async def _get_role_by_id(self, role_id: int) -> RoleDB:
        result = await self.db.execute(select(RoleDB).where(RoleDB.id == role_id))
        role_db = result.scalar_one_or_none()
        if role_db is None:
            raise RoleNotFound()
        return role_db

    async def get_role_by_rolename(self, rolename: str) -> RoleDB:
        result = await self.db.execute(select(RoleDB).where(RoleDB.name == rolename))
        role_db = result.scalar_one_or_none()
        if role_db is None:
            raise RoleNotFound()
        return role_db

    async def get_role(self, role_id: int) -> RoleRead:
        role_db = await self._get_role_by_id(role_id)
        return RoleRead.model_validate(role_db)

    async def create_role(self, role: RoleCreate) -> RoleRead:
        role_db = RoleDB(
            name=role.name, description=role.description, permissions=role.permissions
        )
        self.db.add(role_db)
        try:
            await self.db.commit()
            await self.db.refresh(role_db)
        except IntegrityError:
            await self.db.rollback()
            raise RoleAlreadyExists()
        return RoleRead.model_validate(role_db)

    async def update_role(self, role_id: int, role: RoleUpdate) -> RoleRead:
        role_db = await self._get_role_by_id(role_id)
        role_db.name = role.name
        role_db.description = role.description
        role_db.permissions = list(map(str, role.permissions))
        await self.db.commit()
        await self.db.refresh(role_db)
        return RoleRead.model_validate(role_db)

    async def delete_role(self, role_id: int) -> RoleDeleted:
        role_db = await self._get_role_by_id(role_id)
        await self.db.delete(role_db)
        await self.db.commit()
        return RoleDeleted.model_validate(role_db)
