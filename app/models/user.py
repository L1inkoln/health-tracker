from sqlalchemy import Integer, DateTime, BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from .base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, nullable=False, unique=True)
    start_date: Mapped[DateTime] = mapped_column(DateTime, default=func.now())

    health: Mapped["Health"] = relationship(  # type: ignore  # noqa: F821
        "Health", back_populates="user", uselist=False
    )
    sleep: Mapped["Sleep"] = relationship("Sleep", back_populates="user", uselist=False)  # type: ignore  # noqa: F821
    nutrition: Mapped["Nutrition"] = relationship(  # type: ignore  # noqa: F821
        "Nutrition", back_populates="user", uselist=False
    )
