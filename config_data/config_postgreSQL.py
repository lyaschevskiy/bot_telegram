import psycopg2
from psycopg2 import OperationalError
from config_data.config import Config, load_config
from config_data.config_db_sqlite import create_table_users


def create_connection_postgres():
    """create_connection_postgres"""
    config: Config = load_config()
    connection = None
    try:
        connection = psycopg2.connect(
            host=config.base_postgresql.db_host,
            database=config.base_postgresql.db_proverka,
            user=config.base_postgresql.db_user,
            password=config.base_postgresql.db_password,
            port=config.base_postgresql.db_port)
    except OperationalError as e:
        print(e)
    return connection


def create_connection_db():
    """create connection db"""
    config: Config = load_config()
    connection = None
    try:
        connection = psycopg2.connect(
            host=config.base_postgresql.db_host,
            database=config.base_postgresql.db_name,
            user=config.base_postgresql.db_user,
            password=config.base_postgresql.db_password,
            port=config.base_postgresql.db_port)
    except OperationalError as e:
        print(e)
    return connection


def create_db_and_table() -> None:
    """create db and table"""
    config: Config = load_config()
    answer = False
    connection = None
    try:
        connection = create_connection_postgres()
        connection.autocommit = True
        # connection.commit()
        with connection.cursor() as cursor:
            cursor.execute("SELECT datname FROM pg_database;")
            results = cursor.fetchall()
            for result in results:
                if (result[0]) == config.base_postgresql.db_name:
                    answer = True
                    break
            if not answer:
                cursor.execute(f"CREATE DATABASE {config.base_postgresql.db_name};")
                print(f"Создана БД: {config.base_postgresql.db_name}")
            cursor.execute(create_table_users)
    except Exception as e:
        print(e)
    except OperationalError as e:
        print(e)
    finally:
        if connection:
            connection.close()

    connection = None
    try:
        connection = create_connection_db()
        connection.autocommit = True
        if not answer:
            with connection.cursor() as cursor:
                cursor.execute(create_table_users)
                print(f"Создана таблица пользователи")
    finally:
        if connection:
            connection.close()


def execute_query(query):
    """execute_query"""
    connection = None
    try:
        connection = create_connection_db()
        connection.autocommit = True
        with connection.cursor() as cursor:
            cursor.execute(query)
    except OperationalError as e:
        print(f"The error modify: '{e}'")
    finally:
        if connection:
            connection.close()


def execute_read_query(query):
    """execute_read_query"""
    try:
        connection = create_connection_db()
        with connection.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
            connection.close()
            return result
    except OperationalError as e:
        print(f"The error select: '{e}'")


if __name__ == '__main__':
    create_db_and_table()
    kavuchka = "'"
    id_telega = 1222
    nickname = 'nick'
    phone = '+38097'
    status = True
    sql = (f' INSERT INTO Users\n'
           f' (id_telega, nickname, phone, status)\n'
           f' VALUES ({id_telega}, {kavuchka}{nickname}{kavuchka},'
           f' {kavuchka}{phone}{kavuchka}, {status});')
    execute_query(sql)
