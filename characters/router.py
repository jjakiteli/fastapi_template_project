from typing import List

from fastapi import APIRouter

from characters.dependencies import CharacterRepo
from characters.models import (
    CharacterCreate,
    CharacterDeleted,
    CharacterRead,
    CharacterUpdate,
)
from roles.dependencies import (
    DeleteCharacterPermission,
    ReadCharacterPermission,
    UpdateCharacterPermission,
)
from users.dependencies import CurrentUserDB

router = APIRouter(prefix="/characters", tags=["Characters"])
sub_router = APIRouter(prefix="", tags=["Characters"])


@router.get("/")
async def get_all_characters(
    character_repo: CharacterRepo, permission: ReadCharacterPermission
) -> List[CharacterRead]:
    return await character_repo.get_all_characters()


@router.put("/{character_id}")
async def update_character(
    character_id: int,
    character: CharacterUpdate,
    character_repo: CharacterRepo,
    permission: UpdateCharacterPermission,
) -> CharacterRead:
    return await character_repo.update_character(character_id, character)


@router.patch("/{character_id}/exp")
async def edit_character_exp(
    id: int,
    exp_added: int,
    character_repo: CharacterRepo,
    permission: UpdateCharacterPermission,
) -> CharacterRead:
    return await character_repo.edit_character_exp(id, exp_added)


@router.delete("/{character_id}")
async def delete_character(
    id: int, character_repo: CharacterRepo, permission: DeleteCharacterPermission
) -> CharacterDeleted:
    return await character_repo.delete_character(id)


@sub_router.get("/me/characters")
async def get_characters_me(
    currect_user_db: CurrentUserDB, character_repo: CharacterRepo
) -> List[CharacterRead]:
    return await character_repo.get_user_characters(currect_user_db.id)


@sub_router.get("/me/characters/{character_id}")
async def get_character_me(
    character_id: int, character_repo: CharacterRepo
) -> CharacterRead:
    return await character_repo.get_character(character_id)


@sub_router.post("/me/characters")
async def create_character_me(
    character: CharacterCreate,
    currect_user_db: CurrentUserDB,
    character_repo: CharacterRepo,
) -> CharacterRead:
    return await character_repo.create_character(currect_user_db.id, character)


@sub_router.put("/me/characters/{character_id}")
async def update_character_me(
    character_id: int,
    character: CharacterUpdate,
    currect_user_db: CurrentUserDB,
    character_repo: CharacterRepo,
) -> CharacterRead:
    return await character_repo.update_character(character_id, character)


@sub_router.delete("/me/characters/{character_id}")
async def delete_character_me(
    character_id: int, currect_user_db: CurrentUserDB, character_repo: CharacterRepo
) -> CharacterDeleted:
    return await character_repo.delete_character(character_id)
