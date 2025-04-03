from sqlalchemy import Integer, DateTime, Float, Date
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.sql import func


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    telegram_id: Mapped[int] = mapped_column(Integer, nullable=False, unique=True)
    start_date: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    target_calories: Mapped[int] = mapped_column(
        Integer, default=2000
    )  # Пример по умолчанию
    target_water: Mapped[float] = mapped_column(Integer, default=2.0)  # В литрах
    target_sleep: Mapped[int] = mapped_column(Integer, default=8)  # Часы
    created_at: Mapped[DateTime] = mapped_column(
        DateTime, default=func.now(), nullable=False
    )
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime, default=func.now(), onupdate=func.now(), nullable=False
    )


class Nutrition(Base):
    __tablename__ = "nutrition"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, nullable=False)
    calories: Mapped[int] = mapped_column(Integer, nullable=False)
    water: Mapped[float] = mapped_column(Float, nullable=False)
    date: Mapped[Date] = mapped_column(Date, nullable=False)


class Sleep(Base):
    __tablename__ = "sleep"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, nullable=False)
    hours: Mapped[int] = mapped_column(Integer, nullable=False)
    date: Mapped[Date] = mapped_column(Date, nullable=False)


class Health(Base):
    __tablename__ = "health"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, nullable=False)
    steps: Mapped[int] = mapped_column(Integer, nullable=False)
    date: Mapped[Date] = mapped_column(Date, nullable=False)
