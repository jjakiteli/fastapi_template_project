from datetime import datetime

from pydantic import BaseModel
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from database.models import Base
from enums.hero_classes import HeroClass


class CharacterCreate(BaseModel):
    name: str = "required*"
    hero_class: HeroClass


class CharacterUpdate(BaseModel):
    name: str = "required*"


class CharacterRead(BaseModel):
    id: int
    owner_id: int
    name: str
    hero_class: HeroClass
    level: int
    exp: int
    last_active: datetime

    class Config:
        from_attributes = True


class CharacterDeleted(BaseModel):
    id: int
    owner_id: int
    name: str
    hero_class: HeroClass
    level: int
    exp: int
    last_active: datetime

    class Config:
        from_attributes = True


class CharacterDB(Base):
    __tablename__ = "characters"

    id: Mapped[int] = mapped_column(primary_key=True)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    hero_class: Mapped[str] = mapped_column(nullable=False)
    level: Mapped[int] = mapped_column(nullable=False, default=1)
    exp: Mapped[int] = mapped_column(nullable=False, default=0)
    last_active: Mapped[datetime] = mapped_column(
        nullable=False, default=datetime.now()
    )
