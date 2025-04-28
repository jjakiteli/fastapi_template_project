from datetime import datetime, timedelta
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from bans.exceptions import UserNotBanned
from bans.models import BanDB, BanRead
from users.exceptions import UserNotFound
from users.models import UserDB


class BansRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def ban_user(
        self, user_id: int, duration: Optional[int] | None, reason: str
    ) -> BanRead:
        if duration:
            end_time = datetime.now() + timedelta(seconds=duration)
        else:
            end_time = None

        result = await self.db.execute(select(UserDB).where(UserDB.id == user_id))
        user_db = result.scalars().first()
        if user_db is None:
            raise UserNotFound()

        result = await self.db.execute(select(BanDB).where(BanDB.user_id == user_id))
        ban_db = result.scalars().first()

        if ban_db:
            ban_db.expires_at = end_time
            ban_db.reason = reason
        else:
            ban_db = BanDB(user_id=user_id, expires_at=end_time, reason=reason)
            self.db.add(ban_db)

        user_db.is_active = False

        await self.db.commit()
        await self.db.refresh(ban_db)
        return BanRead.model_validate(ban_db)

    async def unban_user(self, user_id: int) -> BanRead:
        result = await self.db.execute(select(UserDB).where(UserDB.id == user_id))
        user_db = result.scalars().first()
        if user_db is None:
            raise UserNotFound()

        result = await self.db.execute(select(BanDB).where(BanDB.user_id == user_id))
        ban_db = result.scalars().first()
        if ban_db is None:
            raise UserNotBanned()

        await self.db.delete(ban_db)
        user_db.is_active = True

        await self.db.commit()
        return BanRead.model_validate(ban_db)

    async def ban_cleanup_task(self):
        result = await self.db.execute(
            select(BanDB).where(BanDB.expires_at <= datetime.now())
        )
        expired_bans = result.scalars().all()

        for ban in expired_bans:
            await self.unban_user(ban.user_id)
