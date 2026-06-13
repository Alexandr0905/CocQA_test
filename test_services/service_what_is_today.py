# Modul_4\Cinescope\tests\api\test_mock_services.py

import datetime
import pytz
import requests
from constants import AUTH_BASE_URL, HEADERS, REGISTER_ENDPOINT, LOGIN_ENDPOINT
from custom_requester.custom_requester import CustomRequest
from api.api_manager import ApiManager
from constants import Roles
from models.base_models import RegisterUserResponse, TestUser

import requests
from pydantic import BaseModel, Field
from datetime import datetime


# Модель Pydantic для ответа сервера worldclockapi
class WorldClockResponse(BaseModel):
    id: str = Field(alias="$id")  # Используем алиас для поля "$id"
    currentDateTime: str
    utcOffset: str
    isDayLightSavingsTime: bool
    dayOfTheWeek: str
    timeZoneName: str
    currentFileTime: int
    ordinalDate: str
    serviceResponse: None

    class Config:
        # Разрешаем использование алиасов при парсинге JSON
        allow_population_by_field_name = True


# Модель для запроса к сервису TodayIsHoliday
class DateTimeRequest(BaseModel):
    currentDateTime: str  # Формат: "2025-02-13T21:43Z"


# Модель для ответа от сервиса TodayIsHoliday
class WhatIsTodayResponse(BaseModel):
    message: str


# Функция выолняющая запрос в сервис worldclockapi для получения текущей даты
def get_worldclockap_time() -> WorldClockResponse:
    # Выполняем GET-запрос
    response = requests.get("http://worldclockapi.com/api/json/utc/now")  # Запрос в реальный сервис
    # Проверяем статус ответа
    assert response.status_code == 200, "Удаленный сервис недоступен"
    # Парсим JSON-ответ с использованием Pydantic модели
    return WorldClockResponse(**response.json())


class TestTodayIsHolidayServiceAPI:
    # worldclockap
    def test_worldclockap(self):  # проверка работоспособности сервиса worldclockap
        world_clock_response = get_worldclockap_time()
        # Выводим текущую дату и время
        current_date_time = world_clock_response.currentDateTime
        print(f"Текущая дата и время: {current_date_time=}")

        assert current_date_time == datetime.now(pytz.utc).strftime("%Y-%m-%dT%H:%MZ"), "Дата не совпадает"

    def test_what_is_today(self):  # проверка работоспособности Fake сервиса what_is_today
        # Запрашиваем текущее время у сервиса worldclockap
        world_clock_response = get_worldclockap_time()

        what_is_today_response = requests.post("http://127.0.0.1:16002/what_is_today",
                                               data=DateTimeRequest(
                                                   currentDateTime=world_clock_response.currentDateTime).model_dump_json()
                                               )

        # Проверяем статус ответа от тестируемогосервиса
        assert what_is_today_response.status_code == 200, "Удаленный сервис недоступен"
        # Парсим JSON-ответ от тестируемого сервиса с использованием Pydantic модели
        what_is_today_data = WhatIsTodayResponse(**what_is_today_response.json())
        # Проводим валидацию ответа тестируемого сервиса
        assert what_is_today_data.message == "Сегодня нет праздников в России.", "Сегодня нет праздника!"
