from typing import Annotated

from fastapi import Depends

from characters.repository import CharacterRepository
from database.dependencies import DatabaseSession


async def get_character_repo(db: DatabaseSession) -> CharacterRepository:
    return CharacterRepository(db)


CharacterRepo = Annotated[CharacterRepository, Depends(get_character_repo)]
