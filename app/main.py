from fastapi import FastAPI
from app.routers import user, nutrition, sleep, health

# from app.session import init_db


app = FastAPI(title="Healthbot")

# Подключаем маршруты
app.include_router(user.router)
app.include_router(nutrition.router)
app.include_router(sleep.router)
app.include_router(health.router)
