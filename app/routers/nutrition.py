from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.models import Nutrition
from app.schemas.nutrition import NutritionSchema
from app.session import get_db
from app.verify import verify_token

router = APIRouter(tags=["users"])


# Поиск по tg id и обновление значения
@router.post(
    "/nutrition/", dependencies=[Depends(verify_token)], response_model=NutritionSchema
)
def add_nutrition(nutrition: NutritionSchema, db: Session = Depends(get_db)):
    db_nutrition = (
        db.query(Nutrition)
        .filter(Nutrition.user_telegram_id == nutrition.user_telegram_id)
        .first()
    )
    if not db_nutrition:
        raise HTTPException(status_code=404, detail="User not found")
    db_nutrition.calories += nutrition.calories
    db_nutrition.water += nutrition.water
    db.commit()
    db.refresh(db_nutrition)
    return db_nutrition
