from typing import List

from pydantic import BaseModel
from sqlalchemy import JSON
from sqlalchemy.orm import Mapped, mapped_column

from database.models import Base
from enums.permissions import Permission


class RoleCreate(BaseModel):
    name: str = "required*"
    description: str = ""
    permissions: List[Permission]


class RoleUpdate(BaseModel):
    name: str = "required*"
    description: str = ""
    permissions: List[Permission]


class RoleRead(BaseModel):
    id: int
    name: str = "required*"
    description: str = ""
    permissions: List[Permission]

    class Config:
        from_attributes = True


class RoleDeleted(BaseModel):
    id: int
    name: str = "required*"
    description: str = ""
    permissions: List[Permission]

    class Config:
        from_attributes = True


class RoleDB(Base):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False, unique=True, index=True)
    description: Mapped[str] = mapped_column(nullable=False, default="")
    permissions: Mapped[List[str]] = mapped_column(JSON, nullable=False, default=[])
