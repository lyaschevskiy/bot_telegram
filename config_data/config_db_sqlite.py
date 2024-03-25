# Создание таблицы
# create_tables(config.path_sqlite)

# Добавление пользователя
# add_users(config.path_sqlite,
#           2033166672, 'nick', '+38097000000', True)

# Обновление пользователя
# update_users(config.path_sqlite, False, 2033166672)

# Выборка пользователя
# select_users(config.path_sqlite, 2033166672)

# Удаление пользователя
# delete_users(config.path_sqlite, 2033166672)

import sqlite3
from sqlite3 import Error
from typing import List


def create_connection(path):
    """Connect to base"""
    connection = None
    try:
        # подключение к БД
        connection = sqlite3.connect(path,
                                     detect_types=sqlite3.PARSE_DECLTYPES)
        print(f'Поключение к {path} успешно выполненно')
    except Error as e:
        print(f"Ошибка: {e}")

    return connection


def execute_query(connection, query, *param):
    """Vupolnit zapros"""
    cursor = connection.cursor()
    try:
        cursor.execute(query, *param)  # запрос к БД
        connection.commit()  # фиксирует изменения в БД
        print("Запрос выполнен успешно")
    except Error as e:
        print(f"Ошибка: {e}")


def execute_read_query(connection, query, *param):
    """Read query"""
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query, *param)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"Ошибка: {e}")


def create_tables(path: str) -> None:
    try:
        connections = create_connection(path)
        execute_query(connections, create_table_users)
    except ValueError as e:
        print(f"Ошибка {e}")
    finally:
        if connections:
            connections.close()


def add_users(path: str, id_telega: int,
              nickname: str, phone: str, status: bool) -> None:
    try:
        connections = create_connection(path)
        execute_query(connections,
                      add_users_request,
                      (id_telega, nickname, phone, status))
    except ValueError as e:
        print(f"Ошибка {e}")
    finally:
        if connections:
            connections.close()


def update_users(path: str, status: bool, id_telega: int) -> None:
    try:
        connections = create_connection(path)
        execute_query(connections,
                      update_users_request,
                      (status, id_telega))
    except ValueError as e:
        print(f"Ошибка {e}")
    finally:
        if connections:
            connections.close()


def delete_users(path: str, id_telega: int) -> None:
    try:
        connections = create_connection(path)
        execute_query(connections, delete_users_request, (id_telega,))
    except ValueError as e:
        print(f"Ошибка {e}")
    finally:
        if connections:
            connections.close()


def select_users(path: str, id_telega: int) -> List:
    results = []
    try:
        connections = create_connection(path)
        results = execute_read_query(
            connections, select_users_request, (id_telega,))
    except ValueError as e:
        print(f"Ошибка {e}")
    finally:
        if connections:
            connections.close()
        return results


def select_active_users(path: str) -> List:
    results = []
    try:
        connections = create_connection(path)
        results = execute_read_query(
            connections, select_active_users_request)
    except ValueError as e:
        print(f"Ошибка {e}")
    finally:
        if connections:
            connections.close()
        return results


create_table_users = """
CREATE TABLE IF NOT EXISTS Users (
   id_telega INTEGER PRIMARY KEY NOT NULL,
   nickname CHAR(20) NOT NULL,
   phone CHAR(20) NOT NULL,
   status BOOLEAN NOT NULL
);
"""
add_users_request = """
    INSERT INTO Users
        (id_telega, nickname, phone, status)
    VALUES
        (?, ?, ?, ?);"""

update_users_request = """UPDATE Users
                  SET status = ?
                  WHERE id_telega = ?;"""

delete_users_request = """DELETE FROM Users WHERE id_telega = ?;"""

select_users_request = """SELECT status
                  FROM Users
                  WHERE id_telega = ?;"""

select_active_users_request = """SELECT id_telega
                  FROM Users
                  WHERE status = True;"""

if __name__ == "__main__":
    connection = create_connection('proba_db')
    execute_query(connection, create_table_users)
    connection.close()
