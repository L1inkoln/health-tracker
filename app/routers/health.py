from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.health import Health
from app.schemas.health import HealthSchema
from app.session import get_db
from app.verify import verify_token

router = APIRouter(tags=["users"])


# Поиск по tg id и обновление значения
@router.post(
    "/health/", dependencies=[Depends(verify_token)], response_model=HealthSchema
)
def add_health(nutrition: HealthSchema, db: Session = Depends(get_db)):
    db_health = (
        db.query(Health)
        .filter(Health.user_telegram_id == nutrition.user_telegram_id)
        .first()
    )
    if not db_health:
        raise HTTPException(status_code=404, detail="User not found")
    db_health.steps += nutrition.steps
    db.commit()
    db.refresh(db_health)
    return db_health
