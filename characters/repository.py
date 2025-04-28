from datetime import datetime
from typing import List

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from characters.exceptions import CharacterAlreadyExists, CharacterNotFound
from characters.models import (
    CharacterCreate,
    CharacterDB,
    CharacterDeleted,
    CharacterRead,
    CharacterUpdate,
)


class CharacterRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all_characters(self) -> List[CharacterRead]:
        result = await self.db.execute(select(CharacterDB))
        characters_db = result.scalars().all()
        return [CharacterRead.model_validate(character) for character in characters_db]

    async def get_user_characters(self, user_id: int) -> List[CharacterRead]:
        result = await self.db.execute(
            select(CharacterDB).where(CharacterDB.owner_id == user_id)
        )
        characters_db = result.scalars().all()
        return [CharacterRead.model_validate(character) for character in characters_db]

    async def _get_character_by_id(self, character_id: int) -> CharacterDB:
        result = await self.db.execute(
            select(CharacterDB).where(CharacterDB.id == character_id)
        )
        character_db = result.scalar_one_or_none()
        if character_db is None:
            raise CharacterNotFound()
        return character_db

    async def get_character(self, character_id: int) -> CharacterRead:
        character_db = await self._get_character_by_id(character_id)
        return CharacterRead.model_validate(character_db)

    async def create_character(
        self, owner_id: int, character: CharacterCreate
    ) -> CharacterRead:
        character_db = CharacterDB(
            owner_id=owner_id,
            name=character.name,
            hero_class=character.hero_class,
            last_active=datetime.now(),
        )
        self.db.add(character_db)
        try:
            await self.db.commit()
            await self.db.refresh(character_db)
        except IntegrityError:
            await self.db.rollback()
            raise CharacterAlreadyExists()
        return CharacterRead.model_validate(character_db)

    async def update_character(
        self, character_id: int, character: CharacterUpdate
    ) -> CharacterRead:
        character_db = await self._get_character_by_id(character_id)
        character_db.name = character.name
        await self.db.commit()
        await self.db.refresh(character_db)
        return CharacterRead.model_validate(character_db)

    async def edit_character_exp(
        self, character_id: int, exp_added: int
    ) -> CharacterRead:
        exp_per_level = 10
        character_db = await self._get_character_by_id(character_id)
        character_db.exp += exp_added
        levels_added = character_db.exp // exp_per_level
        character_db.exp %= exp_per_level
        character_db.level += levels_added
        await self.db.commit()
        await self.db.refresh(character_db)
        return CharacterRead.model_validate(character_db)

    async def delete_character(self, character_id: int) -> CharacterDeleted:
        character_db = await self._get_character_by_id(character_id)
        await self.db.delete(character_db)
        await self.db.commit()
        return CharacterDeleted.model_validate(character_db)
