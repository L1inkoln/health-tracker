from celery import Celery
from sqlalchemy.orm import Session
from app.session import SessionLocal
from app.models.models import Nutrition, Sleep, Health

celery_app = Celery("tasks", broker="amqp://user:newpassword@localhost//")


@celery_app.task
def reset_daily_data():
    db: Session = SessionLocal()

    try:
        db.query(Nutrition).update({Nutrition.calories: 0, Nutrition.water: 0})
        db.query(Sleep).update({Sleep.hours: 0})
        db.query(Health).update({Health.steps: 0})
        db.commit()

    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()
