import pytest

@pytest.fixture
def db_connection():
    # Установка соединения
    connection = "Подключение к БД"
    yield connection  # Передача соединения в тест
    # Очистка ресурсов после теста
    print("Закрытие соединения")

def test_example(db_connection):
    assert db_connection == "Подключение к БД"

