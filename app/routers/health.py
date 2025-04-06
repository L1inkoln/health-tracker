from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models.models import Health
from app.schemas.health import HealthSchema
from app.session import get_db
from app.auth import verify_token

router = APIRouter(tags=["users"])


@router.post(
    "/health/", dependencies=[Depends(verify_token)], response_model=HealthSchema
)
def add_health(nutrition: HealthSchema, db: Session = Depends(get_db)):
    # Ищем существующую запись по telegram_id
    db_health = (
        db.query(Health)
        .filter(Health.user_telegram_id == nutrition.user_telegram_id)
        .first()
    )
    if db_health:
        # Если запись существует, прибавляем новые часы к уже существующим
        db_health.steps += nutrition.steps
    else:
        db_health = Health(**nutrition.model_dump())
        db.add(nutrition)
    db.commit()
    db.refresh(db_health)
    return db_health
