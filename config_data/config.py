from dataclasses import dataclass
from environs import Env


@dataclass
class TgBot:
    token: str  # Токен для доступа к телеграм-боту
    name: str
    user_name: str
    admin_ids: list[int]  # Список id администраторов бота


@dataclass
class DatabaseConfigPostgresql:
    db_proverka: str  # Существующая БД
    db_name: str  # Название базы данных для бота
    db_host: str  # URL-адрес базы данных
    db_port: int  # Port
    db_user: str  # Username пользователя базы данных
    db_password: str  # Пароль к базе данных


@dataclass
class DatabaseConfigSqlite:
    path_sqlite: str  # Путь к базе данных


@dataclass
class Sale:
    path_img_sale: str  # Путь к изображению


@dataclass
class Config:
    tg_bot: TgBot
    base_postgresql: DatabaseConfigPostgresql
    path_sqlite: DatabaseConfigSqlite
    path_img_sale: Sale


# Создаем функцию, которая будет читать файл .env и возвращать
# экземпляр класса Config с заполненными полями token и admin_ids
def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)
    return Config(
        tg_bot=TgBot(
            token=env('BOT_TOKEN'),
            name=env('BOT_NAME'),
            user_name=env('BOT_USERNAME'),
            admin_ids=list(map(int, env.list('ADMIN_IDS')))
        ),
        base_postgresql=DatabaseConfigPostgresql(
            db_proverka=env('POSTGRES_DB_PROVERKA'),
            db_name=env('POSTGRES_DB'),
            db_host=env('POSTGRES_HOST'),
            db_port=env('POSTGRES_HOST_PORT'),
            db_user=env('POSTGRES_USER'),
            db_password=env('POSTGRES_PASSWORD')
        ),
        path_sqlite=DatabaseConfigSqlite(env('SQLITE_PATH')),
        path_img_sale=env('IMG_PATH')
    )
