from api.api_manager import ApiManager
import requests
import pytest

from entities.user import User
from models.base_models import TestUser, CreateUserData, Review_Data
from utils.data_generator import DataGenerator
from resources.user_creds import SuperAdminCreds
from constants import Roles

from sqlalchemy.orm import Session
from db_requester.db_client import get_db_session
from db_requester.db_helpers import DBHelper


@pytest.fixture
def test_user() -> TestUser:
    random_password = DataGenerator.generate_random_password()

    return TestUser(
        email=DataGenerator.generate_random_email(),
        fullName=DataGenerator.generate_random_name(),
        password=random_password,
        passwordRepeat=random_password,
        roles=[Roles.USER]
    )


@pytest.fixture(scope="session")
def session():
    http_session = requests.Session()
    yield http_session
    http_session.close()


@pytest.fixture
def user_session():
    user_pool = []

    def _create_user_session():
        session = requests.Session()
        user_session = ApiManager(session)
        user_pool.append(user_session)
        return user_session

    yield _create_user_session

    for user in user_pool:
        user.close_session()


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


@pytest.fixture
def super_admin(user_session):
    new_session = user_session()

    super_admin = User(
        SuperAdminCreds.USERNAME,
        SuperAdminCreds.PASSWORD,
        [Roles.SUPER_ADMIN],
        new_session
    )

    super_admin.api.auth_api.authenticate(super_admin.creds)
    return super_admin


@pytest.fixture(scope="function")
def creation_user_data(test_user) -> CreateUserData:
    return CreateUserData(
        email=test_user.email,
        fullName=test_user.fullName,
        password=test_user.password,
        passwordRepeat=test_user.passwordRepeat,
        roles=test_user.roles,
        verified=True,
        banned=False
    )


@pytest.fixture
def common_user(user_session, super_admin, creation_user_data):
    new_session = user_session()

    common_user = User(
        creation_user_data.email,
        creation_user_data.password,
        [Roles.USER],
        new_session
    )

    super_admin.api.user_api.create_user(creation_user_data)
    common_user.api.auth_api.authenticate(common_user.creds)
    return common_user


@pytest.fixture
def admin(user_session, super_admin, creation_user_data):
    new_session = user_session()

    admin = User(
        creation_user_data.email,
        creation_user_data.password,
        [Roles.ADMIN],
        new_session
    )

    super_admin.api.user_api.create_user(creation_user_data)
    admin.api.auth_api.authenticate(admin.creds)
    return admin


@pytest.fixture
def movie_payload():
    return {
        "name": DataGenerator.generate_film_name(),
        "imageUrl": DataGenerator.generate_film_url(),
        "price": DataGenerator.generate_film_price(),
        "description": DataGenerator.generate_film_description(),
        "location": DataGenerator.generate_film_location(),
        "published": DataGenerator.generate_film_published(),
        "genreId": 2
    }


@pytest.fixture
def random_movie_price():
    return DataGenerator.generate_film_price()


@pytest.fixture(scope="session")
def movies_query_params():
    return {
        "pageSize": DataGenerator.generate_film_page_size(),
        "page": DataGenerator.generate_film_page_num(),
        "minPrice": DataGenerator.generate_film_min_price(),
        "maxPrice": DataGenerator.generate_film_max_price(),
        "location": DataGenerator.generate_film_location(),
        "published": DataGenerator.generate_film_published(),
        "genreId": DataGenerator.generate_film_genre_id(),
        "createdAt": DataGenerator.generate_film_created_at()
    }


@pytest.fixture(scope="session")
def get_movie_id():
    return DataGenerator.generate_film_id()


@pytest.fixture
def get_created_movie_id(super_admin, movie_payload):
    response = super_admin.api.movies_api.create_movie(movie_payload, expected_status=201)
    return response.json()["id"]


@pytest.fixture(scope="module")
def db_session() -> Session:
    db_session = get_db_session()
    yield db_session
    db_session.close()

@pytest.fixture(scope="function")
def db_helper(db_session) -> DBHelper:
    db_helper = DBHelper(db_session)
    return db_helper

@pytest.fixture(scope="function")
def created_test_user(db_helper):
    user = db_helper.create_test_user(DataGenerator.generate_user_data())
    yield user
    if db_helper.get_user_by_id(user.id):
        db_helper.delete_user(user)

@pytest.fixture(scope="function")
def movie_data():
    return DataGenerator.generate_movie_data()


@pytest.fixture
def db_movie_lifecycle(super_admin, movie_payload):
    response = super_admin.api.movies_api.create_movie(movie_payload)
    movie_id = response.json()["id"]

    yield movie_id, movie_payload

    super_admin.api.movies_api.delete_movie(movie_id)

@pytest.fixture
def registered_user(unauthorized_api_manager, test_user):
    unauthorized_api_manager.auth_api.register_user(test_user)
    return test_user

@pytest.fixture
def review_data() -> Review_Data:
    return Review_Data(
        text=DataGenerator.generate_review_description(),
        rating=DataGenerator.generate_review_rating()
    )