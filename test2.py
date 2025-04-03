from app.celery import celery_app

result = celery_app.send_task("app.tasks.reset_daily_data")
