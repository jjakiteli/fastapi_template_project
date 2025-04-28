from datetime import datetime
from typing import Annotated, Optional

from fastapi import Depends

from bans.repository import BansRepository
from database.dependencies import DatabaseSession


async def get_ban_repo(db: DatabaseSession) -> BansRepository:
    return BansRepository(db)


BanRepo = Annotated[BansRepository, Depends(get_ban_repo)]


async def ban_logging(user_id: int, duration: Optional[int], reason: str):
    now = datetime.now()
    time_now = now.strftime("%Y-%m-%d-%H-%M-%S")
    with open("./db/bans.log", "a") as file:
        file.write(f"{time_now}:: {user_id} is banned for {duration}: {reason}.\n")


async def unban_logging(user_id: int, reason: str):
    now = datetime.now()
    time_now = now.strftime("%Y-%m-%d-%H-%M-%S")
    with open("./db/bans.log", "a") as file:
        file.write(f"{time_now}:: {user_id} is unbanned: {reason}.\n")
