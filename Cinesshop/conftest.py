from Cinesshop.api.api_manager import ApiManager
from constants import BASE_URL, HEADERS, LOGIN_ENDPOINT, REGISTER_ENDPOINT
import requests
import pytest
from utils.data_generator import DataGenerator
from custom_requester.custom_requester import CustomRequest


@pytest.fixture(scope="session")
def test_user():
    random_email = DataGenerator.generate_random_email()
    random_name = DataGenerator.generate_random_name()
    random_password = DataGenerator.generate_random_password()

    return {
        "email": random_email,
        "fullName": random_name,
        "password": random_password,
        "passwordRepeat": random_password,
        "roles": ["USER"]
    }

@pytest.fixture(scope="session")
def test_auth_session(test_user):
    register_url = f"{BASE_URL}/{REGISTER_ENDPOINT}"
    response = requests.post(register_url, json=test_user, headers=HEADERS)
    assert response.status_code == 201, "Пользователь не был создан"

    login_url = f"{BASE_URL}/{LOGIN_ENDPOINT}"
    login_data = {
        "email": test_user["email"],
        "password": test_user["password"]
    }

    response = requests.post(login_url, json=login_data, headers=HEADERS)
    assert response.status_code == 200, "Ошибка авторизации"

    access_token = response.json().get("accessToken")
    assert access_token is not None, "Токен доступа отсутствует"

    session = requests.Session()
    session.headers.update(HEADERS)
    session.headers.update({"Authorization": f"Bearer {access_token}"})
    return session

@pytest.fixture
def requester():
    session = requests.Session()
    return CustomRequest(session=session, base_url=BASE_URL)

@pytest.fixture
def registered_user(requester, test_user):
    response = requester.send_request(method="POST", endpoint=REGISTER_ENDPOINT, data=test_user, expected_status=201)

    response_data = response.json()
    registered_user = test_user.copy()
    registered_user["id"] = response_data["id"]
    return registered_user

@pytest.fixture(scope="session")
def session():
    http_session = requests.Session()
    yield http_session
    http_session.close()

@pytest.fixture(scope="session")
def api_manager(session):
    return ApiManager(session)