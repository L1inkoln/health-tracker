from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from .base import Base


class UserGoals(Base):
    __tablename__ = "user_goals"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_telegram_id: Mapped[int] = mapped_column(
        ForeignKey("users.telegram_id", ondelete="CASCADE"), unique=True, nullable=False
    )
    calories_goal: Mapped[int] = mapped_column(default=2000)
    water_goal: Mapped[float] = mapped_column(default=2.0)
    sleep_goal: Mapped[float] = mapped_column(default=8.0)
    steps_goal: Mapped[int] = mapped_column(default=5000)

    user: Mapped["User"] = relationship(back_populates="goals")  # type: ignore # noqa: F821
