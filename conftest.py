from api.api_manager import ApiManager
from constants import AUTH_BASE_URL, API_BASE_URL, HEADERS, LOGIN_ENDPOINT, REGISTER_ENDPOINT, MOVIES_ENDPOINT
import requests
import pytest
from utils.data_generator import DataGenerator
from custom_requester.custom_requester import CustomRequest
from api.movies_api import MoviesAPI

@pytest.fixture
def test_user():
    random_password = DataGenerator.generate_random_password()
    return {
        "email": DataGenerator.generate_random_email(),
        "fullName": DataGenerator.generate_random_name(),
        "password": random_password,
        "passwordRepeat": random_password,
        "roles": ["USER"]
    }

@pytest.fixture
def registered_user(requester, test_user):
    response = requester.send_request(method="POST", endpoint=REGISTER_ENDPOINT, data=test_user, expected_status=201)
    response_data = response.json()
    registered_user = test_user.copy()
    registered_user["id"] = response_data["id"]
    return registered_user

@pytest.fixture(scope="session")
def session_user():
    random_password = DataGenerator.generate_random_password()
    return {
        "email": DataGenerator.generate_random_email(),
        "fullName": "Session Admin",
        "password": random_password,
        "passwordRepeat": random_password,
        "roles": ["USER"]
    }

@pytest.fixture(scope="session")
def test_auth_session(session_user):
    register_url = f"{AUTH_BASE_URL}/{REGISTER_ENDPOINT}"
    response = requests.post(register_url, json=session_user, headers=HEADERS)
    assert response.status_code == 201, "Пользователь для сессии не был создан"

    login_url = f"{AUTH_BASE_URL}/{LOGIN_ENDPOINT}"
    login_data = {
        "email": session_user["email"],
        "password": session_user["password"]
    }

    response = requests.post(login_url, json=login_data, headers=HEADERS)
    assert response.status_code == 200, "Ошибка авторизации сессии"

    access_token = response.json().get("accessToken")
    assert access_token is not None, "Токен доступа отсутствует"

    session = requests.Session()
    session.headers.update(HEADERS)
    session.headers.update({"Authorization": f"Bearer {access_token}"})
    return session



@pytest.fixture
def requester():
    session = requests.Session()
    return CustomRequest(session=session, base_url=AUTH_BASE_URL)

@pytest.fixture(scope="session")
def session():
    http_session = requests.Session()
    yield http_session
    http_session.close()

@pytest.fixture(scope="session")
def api_manager(session):
    return ApiManager(session)

@pytest.fixture # (scope="session")
def movie_payload():
    random_name = DataGenerator.generate_film_name()
    random_url = DataGenerator.generate_film_url()
    random_price = DataGenerator.generate_film_price()
    random_description = DataGenerator.generate_film_description()
    random_location = DataGenerator.generate_film_location()
    random_published = DataGenerator.generate_film_published()

    return {
        "name": random_name,
        "imageUrl": random_url,
        "price": random_price,
        "description": random_description,
        "location": random_location,
        "published": random_published,
        "genreId": 1
    }

@pytest.fixture
def random_movie_price():
    random_price = DataGenerator.generate_film_price()
    return random_price

@pytest.fixture(scope="session")
def movies_query_params():
    random_page_size = DataGenerator.generate_film_page_size()
    random_page_num = DataGenerator.generate_film_page_num()
    random_min_price = DataGenerator.generate_film_min_price()
    random_max_price = DataGenerator.generate_film_max_price()
    random_location = DataGenerator.generate_film_location()
    random_published = DataGenerator.generate_film_published()
    random_genre_id = DataGenerator.generate_film_genre_id()
    random_created_at = DataGenerator.generate_film_created_at()

    return {
        "pageSize": random_page_size,
        "page": random_page_num,
        "minPrice": random_min_price,
        "maxPrice": random_max_price,
        "location": random_location,
        "published": random_published,
        "genreId": random_genre_id,
        "createdAt": random_created_at
    }

@pytest.fixture(scope="session")
def get_movie_id():
    random_film_id = DataGenerator.generate_film_id()
    return random_film_id

@pytest.fixture
def superadmin_data():
    return {
        "email": "api1@gmail.com",
        "password": "asdqwe123Q"
    }

@pytest.fixture
def auth_requester():
    session = requests.Session()
    return CustomRequest(session=session, base_url=AUTH_BASE_URL)

@pytest.fixture
def api_requester():
    session = requests.Session()
    return CustomRequest(session=session, base_url=API_BASE_URL)

@pytest.fixture
def superadmin_auth_requester(auth_requester, superadmin_data, api_requester):
    login_response = auth_requester.send_request("POST", LOGIN_ENDPOINT, superadmin_data, 200)

    token = login_response.json().get("accessToken")
    assert token is not None, "Токен не получен при авторизации"

    api_requester.session.headers.update({"Authorization": f"Bearer {token}"})

    return api_requester

@pytest.fixture
def get_created_movie_id(movie_payload, superadmin_auth_requester, api_requester):
    response = superadmin_auth_requester.send_request("POST", MOVIES_ENDPOINT, movie_payload, 201)

    movie_id = response.json()["id"]
    yield movie_id

@pytest.fixture
def movies_api(superadmin_auth_requester):
    from api.movies_api import MoviesAPI
    movies_api = MoviesAPI(session=superadmin_auth_requester.session, base_url=API_BASE_URL)
    return movies_api


@pytest.fixture
def unauthorized_movies_api():
    from api.movies_api import MoviesAPI
    session = requests.Session()
    movies_api = MoviesAPI(session=session, base_url=API_BASE_URL)
    return movies_api