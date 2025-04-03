from celery import Celery
from celery.schedules import crontab


celery_app = Celery(
    "tasks",
    broker="amqp://user:newpassword@localhost//",
    backend="rpc://",  # Использует AMQP для хранения результатов
)

celery_app.conf.update(
    worker_concurrency=1,  # Количество параллельных процессов
    pool="solo",  # Использует один поток (удобно для отладки)
    timezone="Europe/Moscow",
    enable_utc=True,
)


# Планировщик задач
celery_app.conf.beat_schedule = {
    "reset_daily_data": {
        "task": "app.tasks.reset_daily_data",  # Убедись, что путь правильный
        "schedule": crontab(hour=0, minute=0),
    },
}
