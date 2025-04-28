from typing import List

from fastapi import APIRouter

from roles.dependencies import (
    CreateRolePermission,
    DeleteRolePermission,
    ReadRolePermission,
    RoleRepo,
    UpdateRolePermission,
)
from roles.models import RoleCreate, RoleDeleted, RoleRead, RoleUpdate

router = APIRouter(prefix="/roles", tags=["Roles"])


@router.get("/")
async def get_all_roles(
    roles_repo: RoleRepo, permission: ReadRolePermission
) -> List[RoleRead]:
    return await roles_repo.get_all_roles()


@router.get("/{id}")
async def get_role(
    id: int, role_repo: RoleRepo, permission: ReadRolePermission
) -> RoleRead:
    return await role_repo.get_role(id)


@router.post("/")
async def create_role(
    role: RoleCreate, role_repo: RoleRepo, permission: CreateRolePermission
) -> RoleRead:
    return await role_repo.create_role(role)


@router.put("/{id}")
async def update_role(
    id: int, role: RoleUpdate, role_repo: RoleRepo, permission: UpdateRolePermission
) -> RoleRead:
    return await role_repo.update_role(id, role)


@router.delete("/{id}")
async def delete_role(
    id: int, role_repo: RoleRepo, permission: DeleteRolePermission
) -> RoleDeleted:
    return await role_repo.delete_role(id)
