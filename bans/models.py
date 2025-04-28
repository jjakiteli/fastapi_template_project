from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from database.models import Base


class BanRead(BaseModel):
    id: int
    user_id: int
    expires_at: datetime
    reason: str

    class Config:
        from_attributes = True


class BanDB(Base):
    __tablename__ = "bans"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), unique=True, index=True
    )
    expires_at: Mapped[Optional[datetime]] = mapped_column()
    reason: Mapped[str] = mapped_column(nullable=False, default="")
