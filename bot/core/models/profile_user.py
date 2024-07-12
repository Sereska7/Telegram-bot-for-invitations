from typing import TYPE_CHECKING
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from bot.core.models.base import Base

if TYPE_CHECKING:
    from user import User
    from record_event import RecordEvent


class Profile(Base):

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True)
    first_name: Mapped[str] = mapped_column(String(30))
    last_name: Mapped[str] = mapped_column(String(50))
    phone_number: Mapped[str] = mapped_column(String(50))
    position: Mapped[str] = mapped_column(String(50))
    unique_id: Mapped[int]

    user: Mapped["User"] = relationship(back_populates="profile")

    record: Mapped["RecordEvent"] = relationship(back_populates="profile")
