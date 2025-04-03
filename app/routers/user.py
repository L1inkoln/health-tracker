from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.models import User, Nutrition, Sleep, Health
from app.schemas.user import UserSchema
from app.session import get_db

router = APIRouter()


@router.post("/users/", response_model=UserSchema)
def create_user(user: UserSchema, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.telegram_id == user.telegram_id).first()
    if db_user:
        raise HTTPException(status_code=400, detail="User already exists")
    db_user = User(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.get("/statistics/{user_id}", response_model=dict)
def get_statistics(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Статистика по питанию
    nutrition_data = (
        db.query(
            func.sum(Nutrition.calories).label("total_calories"),
            func.sum(Nutrition.water).label("total_water"),
        )
        .filter(Nutrition.user_id == user_id)
        .first()
    )

    # Статистика по сну
    sleep_data = (
        db.query(func.sum(Sleep.hours).label("total_sleep"))
        .filter(Sleep.user_id == user_id)
        .first()
    )

    # Статистика по здоровью
    health_data = (
        db.query(func.sum(Health.steps).label("total_steps"))
        .filter(Health.user_id == user_id)
        .first()
    )

    return {
        "user_id": user_id,
        "total_calories": (
            nutrition_data.total_calories
            if nutrition_data and nutrition_data.total_calories
            else 0
        ),
        "total_water": (
            nutrition_data.total_water
            if nutrition_data and nutrition_data.total_water
            else 0
        ),
        "total_sleep": (
            sleep_data.total_sleep if sleep_data and sleep_data.total_sleep else 0
        ),
        "total_steps": (
            health_data.total_steps if health_data and health_data.total_steps else 0
        ),
    }
