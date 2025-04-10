from app.celery import celery_app
from sqlalchemy.orm import Session
from app.session import SessionLocal
from app.models import Nutrition, Sleep, Health
import logging

logger = logging.getLogger(__name__)


@celery_app.task
def reset_daily_data():
    db: Session = SessionLocal()
    try:
        db.query(Nutrition).update({Nutrition.calories: 0, Nutrition.water: 0})
        db.query(Sleep).update({Sleep.hours: 0})
        db.query(Health).update({Health.steps: 0})
        db.commit()
        logger.info("✅ Ежедневная статистика обновлена успешно.")
    except Exception as e:
        db.rollback()
        logger.error(f"❌ Ошибка при сбросе данных: {e}")
        raise
    finally:
        db.close()
