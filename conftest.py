from api.api_manager import ApiManager
from constants import AUTH_BASE_URL, API_BASE_URL, HEADERS, LOGIN_ENDPOINT, REGISTER_ENDPOINT, MOVIES_ENDPOINT
import requests
import pytest
from utils.data_generator import DataGenerator

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

@pytest.fixture(scope="session")
def session():
    http_session = requests.Session()
    yield http_session
    http_session.close()

@pytest.fixture
def registered_user(api_manager, test_user):
    response = api_manager.auth_api.register_user(test_user, expected_status=201)
    response_data = response.json()
    registered_user = test_user.copy()
    registered_user["id"] = response_data["id"]
    return registered_user

@pytest.fixture(scope="session")
def api_manager(session):
    return ApiManager(session)

@pytest.fixture
def unauthorized_session():
    http_session = requests.Session()
    yield http_session
    http_session.close()

@pytest.fixture
def unauthorized_api_manager(unauthorized_session):
    return ApiManager(unauthorized_session)

@pytest.fixture(scope="session")
def superadmin_user(api_manager, superadmin_data):
    api_manager.auth_api.authenticate(superadmin_data)
    return api_manager

@pytest.fixture(scope="session")
def superadmin_data():
    return ("api1@gmail.com", "asdqwe123Q")

@pytest.fixture
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
def get_created_movie_id(superadmin_user, movie_payload):
    response = superadmin_user.movies_api.create_movie(movie_payload, expected_status=201)
    return response.json()["id"]