import pytest
import requests
from Cinesshop.constants import AUTH_BASE_URL, HEADERS, REGISTER_ENDPOINT,  LOGIN_ENDPOINT, MOVIES_ENDPOINT
from Cinesshop.api.api_manager import ApiManager
# from Cinesshop.custom_requester.custom_requester import CustomRequest


class TestMoviesApiPositive:
    def test_get_movies(self, get_movies, api_requester):
        response = api_requester.send_request("GET", MOVIES_ENDPOINT, get_movies)
        response_data = response.json()

        assert response_data["count"] >= 0," Поле 'count' должно быть числом >= 0"

    def test_get_movies_without_params(self, get_movies, api_requester):
        response = api_requester.send_request("GET", MOVIES_ENDPOINT)
        response_data = response.json()

        assert response_data["count"] >= 0," Поле 'count' должно быть числом >= 0"

    def test_create_movie(self, create_movie, superadmin_auth_requester, api_requester):
        response = superadmin_auth_requester.send_request("POST", MOVIES_ENDPOINT, create_movie, 201)

        movie_id = response.json()["id"]
        get_response = api_requester.send_request("GET", f"{MOVIES_ENDPOINT}/{movie_id}")
        assert response.json()["name"] == get_response.json()["name"], "Параметр названия не сходится"
        assert response.status_code != 400, "Неверные параметры"
        assert response.status_code != 409, "Фильм с таким названием уже существует"

    def test_take_movie(self, get_movie_id, api_requester):
        response = api_requester.send_request("GET", f"{MOVIES_ENDPOINT}/{get_movie_id}")

        assert response.status_code != 404, "Фильм не найден"

    def test_delete_movie(self, get_movie_id, superadmin_auth_requester):
        response = superadmin_auth_requester.send_request("DELETE", f"{MOVIES_ENDPOINT}/{get_movie_id}")

        assert response.status_code != 400, "Неверные параметры"
        assert response.status_code != 404, "Фильм не найден"

    def test_editing_movie(self, get_movie_id, create_movie, superadmin_auth_requester):
        data = {
            "price": create_movie["price"]
        }
        response = superadmin_auth_requester.send_request("PATCH", f"{MOVIES_ENDPOINT}/{get_movie_id}", data)

        assert response.status_code != 400, "Неверные параметры"
        assert response.status_code != 404, "Фильм не найден"

    def test_patch_movie_without_params(self, create_movie, superadmin_auth_requester, get_movie_id):
        movie_id = get_movie_id
        response = superadmin_auth_requester.send_request("PATCH", f"{MOVIES_ENDPOINT}/{movie_id}", expected_status=200)

        assert response.status_code != 400, "Параметры прошли корректно"


class TestMoviesApiNegative:
    class TestMoviesPostRequest:
        def test_create_movie_unauthorized(self, create_movie, superadmin_auth_requester, api_requester):
            response = api_requester.send_request("POST", MOVIES_ENDPOINT, create_movie, 401)
            response_data = response.json()

            assert response_data["message"] == "Unauthorized", f"Ожидали 'Unauthorized', получили '{response_data['message']}'"

        def test_create_movie_without_params(self, create_movie, superadmin_auth_requester, api_requester):
            response = superadmin_auth_requester.send_request("POST", MOVIES_ENDPOINT, expected_status=400)
            response_data = response.json()

            assert response_data["error"] == "Bad Request", f"Ожидали 'Bad Request', получили '{response_data['message']}'"
            assert response.status_code == 400, "Параметры прошли корректно"

        @pytest.mark.parametrize("field, invalid_value", [
            ("name", True),
            ("imageUrl", 2345),
            ("price", None),
            ("description", False),
            ("location", 1234),
            ("published", 1234),
            ("genreId", "1234")  # строка вместо числа
        ])
        def test_create_movie_invalid_types(self, create_movie, superadmin_auth_requester, field, invalid_value):
            data_movie = create_movie.copy()
            data_movie.update({field: invalid_value})

            response = superadmin_auth_requester.send_request("POST", MOVIES_ENDPOINT, data_movie, 400)

            assert response.status_code == 400, f"Ожидали 400 для поля {field} со значением {invalid_value}"
            assert field.lower() in response.text.lower() or "invalid" in response.text.lower()

        @pytest.mark.parametrize("missing_field", [
            "name", "price", "description", "location", "published", "genreId"
        ])
        def test_create_movie_missing_params(self, create_movie, superadmin_auth_requester, missing_field):
            data_movie = create_movie.copy()
            del data_movie[missing_field]

            response = superadmin_auth_requester.send_request("POST", MOVIES_ENDPOINT, data_movie, 400)

            assert response.status_code == 400, f"Сервер должен вернуть 400 при отсутствии поля {missing_field}"

        def test_create_movie_repeat_name(self, create_movie, superadmin_auth_requester):
            data_movie = create_movie.copy()
            data_movie.update({"name": "Название фильма"})

            response = superadmin_auth_requester.send_request("POST", MOVIES_ENDPOINT, data_movie, 409)

            assert response.status_code == 409, f"Сервер должен вернуть 409"
            assert response.json()["error"] == "Conflict", "Отсутствует конфликт при ошибке"

    class TestMoviesIdGetRequest:
        @pytest.mark.parametrize("movie_id, expected_status", [
            ("-1", 404),
            ("abc", 400),
            (" ", 404),
            ("999999999", 404),
            (None, 404)
        ])
        def test_get_movie_invalid_id(self, api_requester, movie_id, expected_status):
            response = api_requester.send_request("GET", f"{MOVIES_ENDPOINT}/{movie_id}", expected_status=expected_status)

            assert response.status_code == expected_status, "Статус код не тот, что ожидали для этого запроса"

    class TestMoviesDeleteRequest:
        @pytest.mark.parametrize("movie_id, expected_status", [
            ("-1", 404),
            ("abc", 404),
            (" ", 404),
            ("999999999", 404),
            (None, 404)
        ])
        def test_delete_movie_invalid_id(self, superadmin_auth_requester, movie_id, expected_status):
            response = superadmin_auth_requester.send_request("DELETE", f"{MOVIES_ENDPOINT}/{movie_id}",
                                                  expected_status=expected_status)

            assert response.status_code == expected_status, "Статус код не тот, что ожидали для этого запроса"

        def test_delete_movie_unauthorize(self, api_requester, get_movie_id):
            movie_id = get_movie_id
            response = api_requester.send_request("DELETE", f"{MOVIES_ENDPOINT}/{movie_id}", expected_status=401)

            assert response.status_code == 401, "Неавторизованный пользователь смог удалить, хотя не должен "

    class TestMoviePatchRequest:
        @pytest.mark.parametrize("movie_id, expected_status", [
            ("-1", 404),
            ("abc", 404),
            (" ", 404),
            ("999999999", 404),
            (None, 404)
        ])
        def test_patch_movie_invalid_id(self, superadmin_auth_requester, movie_id, expected_status):
            response = superadmin_auth_requester.send_request("PATCH", f"{MOVIES_ENDPOINT}/{movie_id}",
                                                  expected_status=expected_status)

            assert response.status_code == expected_status, "Статус код не тот, что ожидали для этого запроса"

        def test_patch_movie_unauthorize(self, api_requester, get_movie_id):
            movie_id = get_movie_id
            response = api_requester.send_request("PATCH", f"{MOVIES_ENDPOINT}/{movie_id}", expected_status=401)

            assert response.status_code == 401, "Неавторизованный пользователь смог удалить, хотя не должен"

        @pytest.mark.parametrize("payload, expected_status", [
            ({"name": ""}, 404),
            ({"imageUrl": 123}, 400),
            ({"price": "free"}, 400),
            ({"description": False}, 400),
            ({"genreId": 99999999}, 404)
        ])
        def test_patch_movie_invalid_body(self, superadmin_auth_requester, payload, expected_status):
            movie_id = 743
            superadmin_auth_requester.send_request("PATCH", f"{MOVIES_ENDPOINT}/{movie_id}", payload, expected_status)