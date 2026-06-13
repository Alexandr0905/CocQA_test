import datetime

import allure
from pytest_check import check

from api.api_manager import ApiManager
from constants import Roles
from models.base_models import TestUser, RegisterUserResponse


@allure.title("Тест регистрации пользователя с помощью Mock")
@allure.severity(allure.severity_level.MINOR)
@allure.label("qa_name", "Ivan Petrovich")
def test_register_user_mock(api_manager: ApiManager, test_user: TestUser, mocker):
    with allure.step(" Мокаем метод register_user в auth_api"):
        mock_response = RegisterUserResponse(  # Фиктивный ответ
            id="id",
            email="email@email.com",
            fullName="fullName",
            verified=True,
            banned=False,
            roles=[Roles.SUPER_ADMIN],
            createdAt=str(datetime.datetime.now())
        )

        mocker.patch.object(
            api_manager.auth_api,  # Объект, который нужно замокать
            'register_user',  # Метод, который нужно замокать
            return_value=mock_response  # Фиктивный ответ
        )

    with allure.step("Вызываем метод, который должен быть замокан"):
        register_user_response = api_manager.auth_api.register_user(test_user)

    with allure.step("Проверяем, что ответ соответствует ожидаемому"):
        with allure.step("Проверка поля персональных данных"):  # обратите внимание на вложенность allure.step
            with check:
                check.equal(register_user_response.fullName, mock_response.fullName, "НЕСОВПАДЕНИЕ fullName")
                check.equal(register_user_response.email, mock_response.email)

        with allure.step("Проверка поля banned"):
            with check("Проверка поля banned"):  # можно использовать вместо allure.step
                check.equal(register_user_response.banned, mock_response.banned)