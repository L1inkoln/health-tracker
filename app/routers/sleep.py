from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models.models import Sleep
from app.schemas.sleep import SleepSchema
from app.session import get_db

router = APIRouter()


@router.post("/sleep/", response_model=SleepSchema)
def add_sleep(sleep: SleepSchema, db: Session = Depends(get_db)):
    db_sleep = Sleep(**sleep.model_dump())
    db.add(db_sleep)
    db.commit()
    db.refresh(db_sleep)
    return db_sleep
