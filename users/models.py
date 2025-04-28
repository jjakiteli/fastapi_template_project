from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from database.models import Base


class UserCreate(BaseModel):
    username: str = "required*"
    password: str = "required*"
    description: str = ""


class UserUpdate(BaseModel):
    username: str = "required*"
    password: str = "required*"
    description: str = ""


class UserRead(BaseModel):
    id: int
    username: str
    description: str
    role: Optional[str]
    is_active: bool
    last_active: datetime

    class Config:
        from_attributes = True


class UserDeleted(BaseModel):
    id: int
    username: str
    description: str
    role: Optional[str]
    is_active: bool
    last_active: datetime

    class Config:
        from_attributes = True


class UserDB(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(nullable=False, unique=True, index=True)
    password: Mapped[str] = mapped_column(nullable=False)  # , repr=False
    description: Mapped[str] = mapped_column(nullable=False, default="")
    role: Mapped[Optional[str]] = mapped_column(
        ForeignKey("roles.name", ondelete="SET NULL"), nullable=True
    )
    is_active: Mapped[bool] = mapped_column(nullable=False, default=True)
    last_active: Mapped[datetime] = mapped_column(
        nullable=False, default=datetime.now()
    )
