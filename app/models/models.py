from sqlalchemy import Integer, DateTime, BigInteger, ForeignKey, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.sql import func


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, nullable=False, unique=True)
    start_date: Mapped[DateTime] = mapped_column(DateTime, default=func.now())

    # Связи с другими таблицами
    health: Mapped["Health"] = relationship(back_populates="user", uselist=False)
    sleep: Mapped["Sleep"] = relationship(back_populates="user", uselist=False)
    nutrition: Mapped["Nutrition"] = relationship(back_populates="user", uselist=False)


class Nutrition(Base):
    __tablename__ = "nutrition"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_telegram_id: Mapped[int] = mapped_column(
        ForeignKey("users.telegram_id", ondelete="CASCADE"), unique=True, nullable=False
    )
    calories: Mapped[int] = mapped_column(Integer, default=0)
    water: Mapped[float] = mapped_column(Float, default=0)

    user: Mapped["User"] = relationship(back_populates="nutrition")


class Sleep(Base):
    __tablename__ = "sleep"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_telegram_id: Mapped[int] = mapped_column(
        ForeignKey("users.telegram_id", ondelete="CASCADE"), unique=True, nullable=False
    )
    hours: Mapped[int] = mapped_column(Integer, default=0)

    user: Mapped["User"] = relationship(back_populates="sleep")


class Health(Base):
    __tablename__ = "health"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_telegram_id: Mapped[int] = mapped_column(
        ForeignKey("users.telegram_id", ondelete="CASCADE"), unique=True, nullable=False
    )
    steps: Mapped[int] = mapped_column(Integer, default=0)

    user: Mapped["User"] = relationship(back_populates="health")
