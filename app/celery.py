from celery import Celery
from datetime import datetime
from app.session import get_db  # Импортируем вашу функцию get_db
from app.models.models import Nutrition, Sleep, Health  # Импортируем модели

celery_app = Celery(
    "tasks",
    broker="redis://localhost:6379/0",
)

celery_app.conf.update(
    timezone="Europe/Moscow",  # Или любой другой часовой пояс
    enable_utc=True,
)


# Задача для сброса статистики
@celery_app.task
def reset_daily_statistics():
    # Получаем сессию базы данных
    db = next(get_db())

    try:
        # Получаем текущую дату для сброса статистики
        now = datetime.now()

        # Очищаем данные по питанию, сну и шагам
        db.query(Nutrition).update({"calories": 0, "water": 0})
        db.query(Sleep).update({"hours": 0})
        db.query(Health).update({"steps": 0})

        # Применяем изменения
        db.commit()

        print(f"Статистика сброшена на {now}")
    finally:
        # Закрываем сессию
        db.close()
