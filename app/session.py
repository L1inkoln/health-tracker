import os

# import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL:
    engine = create_engine(
        DATABASE_URL,
        echo=True,
        pool_size=10,
        max_overflow=20,
        pool_pre_ping=True,
    )
else:
    raise ValueError("DATABASE_URL is not set in environment variables")

# logging.basicConfig(level=logging.INFO)
# logging.info(f"Используемая база данных: {DATABASE_URL}")

# Используем async_sessionmaker для создания сессий
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
