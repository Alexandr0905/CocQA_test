from resources.db_creds import MoviesDbCreds
import psycopg2
from psycopg2 import extras
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from resources.db_creds import MoviesDbCreds

USERNAME = MoviesDbCreds.USERNAME
PASSWORD = MoviesDbCreds.PASSWORD
HOST = MoviesDbCreds.HOST
PORT = MoviesDbCreds.PORT
DATABASE_NAME = MoviesDbCreds.DATABASE_NAME

engine = create_engine(
    f"postgresql+psycopg2://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE_NAME}",
    echo=False  # Установить True для отладки SQL запросов
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db_session():
    return SessionLocal()


# def connect_to_postgres():
#
#     try:
#         with psycopg2.connect(dbname = MoviesDbCreds.dbname,
#             user = MoviesDbCreds.user,
#             password = MoviesDbCreds.password,
#             host = MoviesDbCreds.host,
#             port = MoviesDbCreds.port) as connection:
#             print("Подключение установлено успешно")
#
#             print("Информация о сервере PostgreSQL:")
#             print(connection.get_dsn_parameters(), "\n")
#
#             with connection.cursor() as cursor:
#                 cursor.execute("SELECT version();")
#                 record = cursor.fetchone()
#                 print("Вы подключены к - ", record, "\n")
#
#     except Exception as e:
#         print("Ошибка: ", e)
#
# connect_to_postgres()
#
# def get_users():
#
#     try:
#         with psycopg2.connect(dbname = MoviesDbCreds.dbname,
#             user = MoviesDbCreds.user,
#             password = MoviesDbCreds.password,
#             host = MoviesDbCreds.host,
#             port = MoviesDbCreds.port) as connection:
#             print("Подключение установлено успешно")
#
#             with connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
#                 cursor.execute("SELECT id, full_name FROM users")
#                 first_row = cursor.fetchmany(5)
#                 for row in first_row:
#                     print(f"ID: {row['id']}, Name: {row['full_name']}")
#
#     except Exception as e:
#         print("Ошибка: ", e)
#
# get_users()
#
# def insert_genre():
#
#     try:
#         with psycopg2.connect(dbname = MoviesDbCreds.dbname,
#             user = MoviesDbCreds.user,
#             password = MoviesDbCreds.password,
#             host = MoviesDbCreds.host,
#             port = MoviesDbCreds.port) as connection:
#             print("Подключение установлено успешно")
#
#             with connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
#                 cursor.execute('''
#             INSERT INTO genres (name) VALUES (%s) RETURNING id;
#         ''', ('хуепинание',))
#                 new_id = cursor.fetchone()[0]
#                 print(f"Новая запись создана с ID: {new_id}")
#
#     except Exception as e:
#         print("Ошибка: ", e)
#
# def update_genre():
#
#     try:
#         with psycopg2.connect(dbname = MoviesDbCreds.dbname,
#             user = MoviesDbCreds.user,
#             password = MoviesDbCreds.password,
#             host = MoviesDbCreds.host,
#             port = MoviesDbCreds.port) as connection:
#             print("Подключение установлено успешно")
#
#             with connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
#                 cursor.execute('''
#             UPDATE genres
#             set name = %s
#             where name = %s;
#         ''', ('пиздаболвыблядское пиздаблядскоуебанское страдание', 'хуепинание'))
#                 affected_rows = cursor.rowcount
#                 print(f"Количество обновленных строк: {affected_rows}")
#
#     except Exception as e:
#         print("Ошибка: ", e)
#
# def delete_genre():
#
#     try:
#         with psycopg2.connect(dbname = MoviesDbCreds.dbname,
#             user = MoviesDbCreds.user,
#             password = MoviesDbCreds.password,
#             host = MoviesDbCreds.host,
#             port = MoviesDbCreds.port) as connection:
#             print("Подключение установлено успешно")
#
#             with connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
#                 cursor.execute('''
#                 DELETE from genres
#                 where name = %s;
#                 ''',('пиздаболвыблядское пиздаблядскоуебанское страдание', ))
#                 affected_rows = cursor.rowcount
#                 print(f"Количество обновленных строк: {affected_rows}")
#
#     except Exception as e:
#         print("Ошибка: ", e)
#
# delete_genre()