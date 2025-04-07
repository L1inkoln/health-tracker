from sqlalchemy import Integer, ForeignKey, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base


class Nutrition(Base):
    __tablename__ = "nutrition"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_telegram_id: Mapped[int] = mapped_column(
        ForeignKey("users.telegram_id", ondelete="CASCADE"), unique=True, nullable=False
    )
    calories: Mapped[int] = mapped_column(Integer, default=0)
    water: Mapped[float] = mapped_column(Float, default=0)

    user: Mapped["User"] = relationship(back_populates="nutrition")  # type: ignore  # noqa: F821
