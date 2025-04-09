﻿# Health Tracker Bot

Учебный проект Telegram-бот для трекинга здоровья.

## 📌 Описание проекта
Health Tracker — это учебный backend-сервис для отслеживания состояния здоровья пользователя с интеграцией Telegram-бота. Система позволяет пользователям записывать и анализировать свои показатели: питание, сон и физическую активность.

Проект построен на современном Python-стеке, с акцентом на асинхронность, масштабируемость. Предназначен для запуска в Docker-среде одной командой: docker compose up --build.

![Пример получения статистики](assets/work.png)

## ⚙️ Основной функционал:
- 📲 Telegram-бот:

При старте автоматически регистрирует пользователя в системе.

Поддерживает команды для ввода данных о калориях, воде, сне и шагах.

Команда /reset для обнуления статистики.

Получает JWT-токен при старте и использует его при взаимодействии с API.

- 🚀 REST API на FastAPI:

Эндпоинты для работы с данными: GET, POST, PATCH, DELETE.

Защищённая авторизация через JWT.

Эндпоинт для получения токена Telegram-ботом с проверкой секретного ключа.

- 🛠️ База данных:

PostgreSQL с ORM на SQLAlchemy 2.0.

Использование Alembic для миграций.

Модели разделены от схем на Pydantic v2.

- 🧠 Фоновая логика:

Используется Celery + RabbitMQ для периодического обновления пользовательской статистики (ежедневно в 00:00).

Асинхронное планирование задач без блокировки основного потока приложения.

- 🐳 Docker-окружение:

Полностью контейнеризирован: API, бот, база данных, очередь сообщений.

Запуск в один клик: все миграции и инициализация выполняются автоматически при старте.

## 🏗 Архитектура

health-tracker/

├──/api/ # FastAPI приложение

├──/bot/ # Telegram бот (aiogram)

|── Dockerfile, docker-compose

└── requirements

## 🚀 Запуск проекта
1. **Клонировать репозиторий**:

git clone https://github.com/L1inkoln/health-tracker.git

cd health-tracker

2. **Настроить окружение**:
   
переименовать .env.example в .env и вставить токен телеграм бота в этот файл

3. **Запустить сервисы**:

docker compose up --build

## 📡 Основные API-эндпоинты
GET /user/{tg_id} - Получить полную статистику и рекомендации в соответствии с целью

POST /health /sleep/ nutrition - Добавить значения в ежедневную статистику

PATCH /reset_statistics/{tg_id} - Сброс статистики для пользователя

DELETE /delete/{tg_id} - Удаление пользователя из базы данных

## 🤖 Команды бота
![Меню в телеграме](assets/menu.png)
