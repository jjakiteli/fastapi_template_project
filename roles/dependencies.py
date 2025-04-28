from typing import Annotated, Callable

from fastapi import Depends

from database.dependencies import DatabaseSession
from enums.permissions import Permission
from roles.exceptions import InsufficientPermissions
from roles.repository import RoleRepository
from users.dependencies import CurrentUserDB
from users.models import UserDB


async def get_user_repo(db: DatabaseSession) -> RoleRepository:
    return RoleRepository(db)


RoleRepo = Annotated[RoleRepository, Depends(get_user_repo)]


def get_user_with_role(permission: Permission) -> Callable:
    async def dependency(current_user: CurrentUserDB, role_repo: RoleRepo) -> UserDB:
        if current_user.role is None:
            raise InsufficientPermissions()
        role_db = await role_repo.get_role_by_rolename(current_user.role)
        permissions = [Permission(perm) for perm in role_db.permissions]
        if permission not in permissions and Permission.ADMIN not in permissions:
            raise InsufficientPermissions()
        return current_user

    return dependency


AdminPermission = Annotated[UserDB, Depends(get_user_with_role(Permission.ADMIN))]

ReadRolePermission = Annotated[
    UserDB, Depends(get_user_with_role(Permission.READ_ROLE))
]
CreateRolePermission = Annotated[
    UserDB, Depends(get_user_with_role(Permission.CREATE_ROLE))
]
UpdateRolePermission = Annotated[
    UserDB, Depends(get_user_with_role(Permission.UPDATE_ROLE))
]
DeleteRolePermission = Annotated[
    UserDB, Depends(get_user_with_role(Permission.DELETE_ROLE))
]

ReadUserPermission = Annotated[
    UserDB, Depends(get_user_with_role(Permission.READ_USER))
]
UpdateUserPermission = Annotated[
    UserDB, Depends(get_user_with_role(Permission.UPDATE_USER))
]
DeleteUserPermission = Annotated[
    UserDB, Depends(get_user_with_role(Permission.DELETE_USER))
]
BanUserPermission = Annotated[UserDB, Depends(get_user_with_role(Permission.BAN_USER))]

ReadCharacterPermission = Annotated[
    UserDB, Depends(get_user_with_role(Permission.READ_CHARACTER))
]
UpdateCharacterPermission = Annotated[
    UserDB, Depends(get_user_with_role(Permission.UPDATE_CHARACTER))
]
DeleteCharacterPermission = Annotated[
    UserDB, Depends(get_user_with_role(Permission.DELETE_CHARACTER))
]
