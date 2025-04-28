from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database.database_session import AsyncSessionLocal


async def get_db():
    async with AsyncSessionLocal() as db:
        yield db


DatabaseSession = Annotated[AsyncSession, Depends(get_db)]
