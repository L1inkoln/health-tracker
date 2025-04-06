from fastapi import FastAPI
from app.routers import user, nutrition, sleep, health, auth
import logging

logger = logging.getLogger(__name__)


app = FastAPI(
    title="Healthbot", description="API для Telegram-бота отслеживания здоровья"
)

# Подключаем роуты
app.include_router(user.router)
app.include_router(nutrition.router)
app.include_router(sleep.router)
app.include_router(health.router)
app.include_router(auth.router)
