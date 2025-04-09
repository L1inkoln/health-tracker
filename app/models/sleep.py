from sqlalchemy import Float, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base


class Sleep(Base):
    __tablename__ = "sleep"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_telegram_id: Mapped[int] = mapped_column(
        ForeignKey("users.telegram_id", ondelete="CASCADE"), unique=True, nullable=False
    )
    hours: Mapped[float] = mapped_column(Float, default=0)

    user: Mapped["User"] = relationship(back_populates="sleep")  # type: ignore  # noqa: F821
