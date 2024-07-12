from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from bot.core.models.base import Base

if TYPE_CHECKING:
    from profile import Profile
    from event import Event


class RecordEvent(Base):
    profile_id: Mapped[int] = mapped_column(ForeignKey("profiles.id"))
    event_id: Mapped[int] = mapped_column(ForeignKey("events.id"))

    profile: Mapped["Profile"] = relationship(back_populates="record")

    event: Mapped["Event"] = relationship(back_populates="record")

