from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models.models import Nutrition
from app.schemas.nutrition import NutritionSchema
from app.session import get_db  # Функция для подключения к базе данных

router = APIRouter()


@router.post("/nutrition/", response_model=NutritionSchema)
def add_nutrition(nutrition: NutritionSchema, db: Session = Depends(get_db)):
    # Ищем существующую запись по telegram_id
    db_nutrition = (
        db.query(Nutrition)
        .filter(Nutrition.user_telegram_id == nutrition.user_telegram_id)
        .first()
    )
    if db_nutrition:
        # Если запись существует, прибавляем новые часы к уже существующим
        db_nutrition.calories += nutrition.calories
        db_nutrition.water += nutrition.water
    else:
        db_nutrition = Nutrition(**nutrition.model_dump())
        db.add(nutrition)
    db.commit()
    db.refresh(db_nutrition)
    return db_nutrition
