from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models.models import Nutrition
from app.schemas.nutrition import NutritionSchema
from app.session import get_db  # Функция для подключения к базе данных

router = APIRouter()


@router.post("/nutrition/", response_model=NutritionSchema)
def add_nutrition(nutrition: NutritionSchema, db: Session = Depends(get_db)):
    db_nutrition = Nutrition(**nutrition.model_dump())
    db.add(db_nutrition)
    db.commit()
    db.refresh(db_nutrition)
    return db_nutrition
