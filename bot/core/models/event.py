from datetime import date
from typing import TYPE_CHECKING
from sqlalchemy import String, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship

from bot.core.models.base import Base

if TYPE_CHECKING:
    from record_event import RecordEvent


class Event(Base):
    title: Mapped[str] = mapped_column(String(80))
    description: Mapped[str] = mapped_column(String(255))
    date: Mapped[date] = mapped_column(Date)
    price: Mapped[int]

    record: Mapped["RecordEvent"] = relationship(back_populates="event")
