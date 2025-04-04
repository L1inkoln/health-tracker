from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models.models import Sleep
from app.schemas.sleep import SleepSchema
from app.session import get_db

router = APIRouter()


@router.post("/sleep/", response_model=SleepSchema)
def add_sleep(sleep: SleepSchema, db: Session = Depends(get_db)):
    # Ищем существующую запись по telegram_id
    db_sleep = (
        db.query(Sleep).filter(Sleep.user_telegram_id == sleep.user_telegram_id).first()
    )
    if db_sleep:
        # Если запись существует, прибавляем новые часы к уже существующим
        db_sleep.hours += sleep.hours
    else:
        # Если записи нет, создаем новую запись
        db_sleep = Sleep(**sleep.model_dump())
        db.add(db_sleep)
    db.commit()
    db.refresh(db_sleep)
    return db_sleep
