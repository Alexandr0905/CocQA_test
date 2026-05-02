from constants import AUTH_BASE_URL, LOGIN_ENDPOINT


class TestAuthAPI:
    def test_register_user(self, api_manager, test_user):
        response = api_manager.auth_api.register_user(test_user)
        response_data = response.json()

        assert response_data["email"] == test_user["email"], "Email не совпадает"
        assert "id" in response_data, "Отсутствует id пользователя"
        assert "roles" in response_data, "Роли отсутствуют в ответе"
        assert "USER" in response_data["roles"], "Роль юзера отсутствует в ответе"

    def test_register_and_auth_user(self, api_manager, registered_user):
        login_data = {
            "email": registered_user["email"],
            "password": registered_user["password"]
        }

        response = api_manager.auth_api.login_user(login_data)
        response_data = response.json()

        assert "accessToken" in response_data, "Отсутствует токен доступа в ответа"
        assert response_data["user"]["email"] == registered_user["email"], "Email не совпадает"

    def test_invalid_password(self, test_user, api_manager):
        response = api_manager.auth_api.register_user(test_user)
        response_data = response.json()
        login_data = {
            "email": response_data["email"],
            "password": "Aa1234567890/dfgFG"
        }

        response = api_manager.auth_api.login_user(login_data, expected_status=401)
        print(f"Response status: {response.status_code}")
        print(f"Response body: {response.text}")
        assert response.status_code == 401 or 500, "ОшибОчка, пароль прошел"

    def test_invalid_email(self, test_user, api_manager):
        response = api_manager.auth_api.register_user(test_user)
        login_data = {
            "email": "huepinanie@mail.ru",
            "password": test_user["password"]
        }

        response = api_manager.auth_api.login_user(login_data, expected_status=401)
        print(f"Response status: {response.status_code}")
        print(f"Response body: {response.text}")
        assert response.status_code == 401, "ОшибОчка, email прошел"

    def test_null_body(self, test_user, api_manager):
        login_url = f"{AUTH_BASE_URL}/{LOGIN_ENDPOINT}"
        response = api_manager.session.post(login_url)
        print(f"Response status: {response.status_code}")
        print(f"Response body: {response.text}")
        assert response.status_code == 401, "ОшибОчка тела запроса"