from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.models import Sleep
from app.schemas.sleep import SleepSchema
from app.session import get_db
from app.auth import verify_token

router = APIRouter(tags=["users"])


# Обновление часов сна для пользователя
@router.post(
    "/sleep/", dependencies=[Depends(verify_token)], response_model=SleepSchema
)
def add_sleep(sleep: SleepSchema, db: Session = Depends(get_db)):
    db_sleep = (
        db.query(Sleep).filter(Sleep.user_telegram_id == sleep.user_telegram_id).first()
    )
    if not db_sleep:
        raise HTTPException(status_code=404, detail="User not found")
    db_sleep.hours += sleep.hours
    db.commit()
    db.refresh(db_sleep)
    return db_sleep
