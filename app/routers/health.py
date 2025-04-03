from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models.models import Health
from app.schemas.health import HealthSchema
from app.session import get_db

router = APIRouter()


@router.post("/health/", response_model=HealthSchema)
def add_health(health: HealthSchema, db: Session = Depends(get_db)):
    db_health = Health(**health.model_dump())
    db.add(db_health)
    db.commit()
    db.refresh(db_health)
    return db_health
