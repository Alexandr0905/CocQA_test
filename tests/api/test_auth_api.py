from constants import AUTH_BASE_URL, LOGIN_ENDPOINT
from models.base_models import RegisterUserResponse, LoginData


class TestAuthAPI:
    def test_register_user(self, api_manager, test_user):
        response = api_manager.auth_api.register_user(test_user)
        response_data = RegisterUserResponse(**response.json())

        assert response_data.email == test_user.email, "Email не совпадает"

    def test_register_and_auth_user(self, api_manager, test_user):
        api_manager.auth_api.register_user(test_user)
        login_data = LoginData(
            email=test_user.email,
            password=test_user.password
        )

        response = api_manager.auth_api.login_user(login_data)
        response_data = response.json()

        assert "accessToken" in response_data, "Отсутствует токен доступа в ответе"
        assert response_data["user"]["email"] == test_user.email, "Email не совпадает"

    def test_invalid_password(self, test_user, api_manager):
        api_manager.auth_api.register_user(test_user)
        login_data = LoginData(
            email=test_user.email,
            password="Aa1234567890/dfgFG"
        )

        response = api_manager.auth_api.login_user(login_data, expected_status=401)
        assert response.status_code == 401, "ОшибОчка, пароль прошел"

    def test_invalid_email(self, test_user, api_manager):
        api_manager.auth_api.register_user(test_user)
        login_data = LoginData(
            email="invalid_user@mail.ru",
            password=test_user.password
        )

        response = api_manager.auth_api.login_user(login_data, expected_status=401)
        assert response.status_code == 401, "ОшибОчка, email прошел"

    def test_null_body(self, api_manager):
        login_url = f"{AUTH_BASE_URL}{LOGIN_ENDPOINT}"
        response = api_manager.session.post(login_url)
        assert response.status_code == 401, "ОшибОчка тела запроса"