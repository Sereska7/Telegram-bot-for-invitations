from typing import TYPE_CHECKING
from sqlalchemy import BigInteger, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from bot.core.models.base import Base

if TYPE_CHECKING:
    from profile import Profile


class User(Base):

    tg_id: Mapped[int] = mapped_column(BigInteger)
    tg_name: Mapped[str] = mapped_column(String(50))

    profile: Mapped["Profile"] = relationship(back_populates="user", uselist=False)
