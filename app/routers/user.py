from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models import User, Nutrition, Sleep, Health
from app.schemas.user import UserSchema
from app.session import get_db
from app.verify import verify_token

router = APIRouter(tags=["users"])


# Добавление нового пользователя и заполнение 0 значениями других таблиц
@router.post(
    "/register/", dependencies=[Depends(verify_token)], response_model=UserSchema
)
def create_user(user: UserSchema, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.telegram_id == user.telegram_id).first()
    if db_user:
        raise HTTPException(status_code=400, detail="User already exists")

    db_user = User(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    # Создаем записи в таблицах health, sleep и nutrition с user_telegram_id
    db_health = Health(user_telegram_id=db_user.telegram_id, steps=0)
    db_sleep = Sleep(user_telegram_id=db_user.telegram_id, hours=0)
    db_nutrition = Nutrition(user_telegram_id=db_user.telegram_id, calories=0, water=0)

    db.add(db_health)
    db.add(db_sleep)
    db.add(db_nutrition)
    db.commit()

    return db_user


# Получение всей статистики по tg id
@router.get(
    "/statistics/{telegram_id}",
    dependencies=[Depends(verify_token)],
    response_model=dict,
)
def get_statistics(telegram_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.telegram_id == telegram_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    # Использование select_from для явного указания начальной таблицы
    data = (
        db.query(
            func.coalesce(func.sum(Nutrition.calories), 0).label("calories"),
            func.coalesce(func.sum(Nutrition.water), 0).label("water"),
            func.coalesce(func.sum(Sleep.hours), 0).label("sleep"),
            func.coalesce(func.sum(Health.steps), 0).label("steps"),
        )
        .select_from(User)
        .outerjoin(Nutrition, Nutrition.user_telegram_id == User.telegram_id)
        .outerjoin(Sleep, Sleep.user_telegram_id == User.telegram_id)
        .outerjoin(Health, Health.user_telegram_id == User.telegram_id)
        .filter(User.telegram_id == telegram_id)
        .first()
    )
    if data is not None:
        return {
            "user_telegram_id": telegram_id,
            "calories": data.calories,
            "water": data.water,
            "sleep": data.sleep,
            "steps": data.steps,
        }


# Обработка команды для сброса статистики
@router.patch("/reset/{telegram_id}", dependencies=[Depends(verify_token)])
def reset_statistics(telegram_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.telegram_id == telegram_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    # Обновляем существующие записи
    db.query(Nutrition).filter(Nutrition.user_telegram_id == telegram_id).update(
        {
            "calories": 0,
            "water": 0.0,
        }
    )
    db.query(Sleep).filter(Sleep.user_telegram_id == telegram_id).update(
        {
            "hours": 0,
        }
    )
    db.query(Health).filter(Health.user_telegram_id == telegram_id).update(
        {
            "steps": 0,
        }
    )
    db.commit()
    return {"detail": "Статистика сброшена до нуля"}
