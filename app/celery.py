from celery import Celery
from celery.schedules import crontab


celery_app = Celery(
    "app",
    broker="amqp://guest:guest@rabbitmq:5672//",
    backend="rpc://",
    include=["app.tasks.reset"],  # указать, где лежат задачи
)

celery_app.conf.update(
    timezone="Europe/Moscow",
    enable_utc=False,
    beat_schedule={
        "reset_daily_data": {
            "task": "app.tasks.reset.reset_daily_data",  # путь к задаче
            "schedule": crontab(hour=0, minute=0),  # обновление в 00:00
        },
    },
)
