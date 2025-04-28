import asyncio
from typing import Optional

from fastapi import APIRouter, BackgroundTasks
from fastapi.responses import JSONResponse

from bans.dependencies import BanRepo, ban_logging, unban_logging
from bans.models import BanRead
from roles.dependencies import BanUserPermission

router = APIRouter(prefix="/users", tags=["Bans"])


@router.patch("/{id}/ban")
async def ban_user(
    id: int,
    duration: Optional[int],
    reason: str,
    user_repo: BanRepo,
    permission: BanUserPermission,
    background_tasks: BackgroundTasks,
) -> BanRead:
    background_tasks.add_task(asyncio.run, ban_logging(id, duration, reason))
    return await user_repo.ban_user(id, duration, reason)


@router.patch("/{id}/unban")
async def unban_user(
    id: int,
    reason: str,
    user_repo: BanRepo,
    permission: BanUserPermission,
    background_tasks: BackgroundTasks,
) -> BanRead:
    background_tasks.add_task(asyncio.run, unban_logging(id, reason))
    return await user_repo.unban_user(id)


@router.patch("/bans/refresh")
async def refresh_bans(
    user_repo: BanRepo,
    permission: BanUserPermission,
    background_tasks: BackgroundTasks,
) -> JSONResponse:
    background_tasks.add_task(asyncio.run, user_repo.ban_cleanup_task())
    return JSONResponse(content={"message": "OK"}, status_code=200)
