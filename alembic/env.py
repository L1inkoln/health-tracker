from logging.config import fileConfig
from sqlalchemy.ext.asyncio import async_engine_from_config, AsyncEngine
from sqlalchemy import pool
from alembic import context
from app.models.models import Base

# Получаем конфиг Alembic
config = context.config

# Настройка логирования
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Метаданные моделей для автогенерации миграций
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Запуск миграций в офлайн-режиме."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    """Запуск миграций в онлайн-режиме с асинхронным движком."""
    config_section = config.get_section(config.config_ini_section)
    if config_section is None:
        raise ValueError("Не удалось загрузить конфигурацию Alembic")

    # Создание асинхронного движка с конфигурацией
    connectable: AsyncEngine = async_engine_from_config(
        config_section,  # Это теперь гарантированно dict[str, Any]
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    # Ожидание подключения и запуск миграций
    async with connectable.connect() as connection:
        await connection.run_sync(
            do_run_migrations
        )  # Вызываем синхронную функцию для миграций


def do_run_migrations(connection):
    """Функция для запуска миграций в синхронном режиме внутри асинхронного контекста."""
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


# Выбор режима (офлайн или онлайн) для выполнения миграций
if context.is_offline_mode():
    run_migrations_offline()
else:
    import asyncio

    # Асинхронный запуск миграций в онлайн-режиме
    asyncio.run(run_migrations_online())
