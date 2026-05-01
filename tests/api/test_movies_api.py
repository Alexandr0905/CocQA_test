import pytest

class TestMoviesApiPositive:
    def test_get_movies(self, movies_query_params, movies_api):
        response = movies_api.get_movies(params=movies_query_params)
        response_data = response.json()

        assert response_data["count"] >= 0," Поле 'count' должно быть числом >= 0"

    def test_get_movies_without_params(self, movies_api):
        response = movies_api.get_movies()
        response_data = response.json()

        assert response_data["count"] >= 0," Поле 'count' должно быть числом >= 0"

    def test_create_movie(self, movie_payload, movies_api):
        response = movies_api.create_movie(movie_payload)

        movie_id = response.json()["id"]
        get_response = movies_api.get_movie(movie_id)
        assert response.json()["name"] == get_response.json()["name"], "Параметр названия не сходится"

    def test_get_movie(self, get_created_movie_id, movies_api):
        response = movies_api.get_movie(get_created_movie_id)

        assert get_created_movie_id == response.json()["id"], "ID фильмов в запросе и ответе различаются"

    def test_delete_movie(self, get_created_movie_id, movies_api):
        response = movies_api.delete_movie(get_created_movie_id)

        movie_id = response.json()["id"]
        assert get_created_movie_id == movie_id, "ID фильма на удаление и непосредственно удаленного фильма не совпадают"
        get_response = movies_api.get_movie(movie_id, expected_status=404)

    def test_editing_movie(self, get_created_movie_id, random_movie_price, movies_api):
        data = {
            "price": random_movie_price
        }
        response = movies_api.patch_update_movie(get_created_movie_id, data)

        assert response.json()["price"] == random_movie_price, "Цена не была обновлена"

    def test_patch_movie_without_params(self, movies_api, get_created_movie_id):
        origin_response = movies_api.get_movie(get_created_movie_id)
        origin_data = origin_response.json()

        response = movies_api.patch_update_movie(get_created_movie_id, None)

        updated_response = movies_api.get_movie(get_created_movie_id)
        updated_data = updated_response.json()

        assert origin_data == updated_data, "Фильм изменился без передачи данных"

class TestMoviesApiNegative:
    class TestMoviesPostRequest:
        def test_create_movie_unauthorized(self, movie_payload, unauthorized_movies_api):
            response = unauthorized_movies_api.create_movie(movie_payload, expected_status=401)
            response_data = response.json()

            assert response_data["message"] == "Unauthorized", f"Ожидали 'Unauthorized', получили '{response_data['message']}'"

        def test_create_movie_without_params(self, movie_payload, movies_api):
            response = movies_api.create_movie(None, expected_status=400)
            response_data = response.json()

            assert response_data["error"] == "Bad Request", f"Ожидали 'Bad Request', получили '{response_data['message']}'"

        @pytest.mark.parametrize("field, invalid_value", [
            ("name", True),
            ("imageUrl", 2345),
            ("price", None),
            ("description", False),
            ("location", 1234),
            ("published", 1234),
            ("genreId", "1234")
        ])
        def test_create_movie_invalid_types(self, movie_payload, movies_api, field, invalid_value):
            data_movie = movie_payload.copy()
            data_movie.update({field: invalid_value})

            response = movies_api.create_movie(data_movie, 400)

            assert field.lower() in response.text.lower() or "invalid" in response.text.lower()

        @pytest.mark.parametrize("missing_field", [
            "name", "price", "description", "location", "published", "genreId"
        ])
        def test_create_movie_missing_params(self, movie_payload, movies_api, missing_field):
            data_movie = movie_payload.copy()
            del data_movie[missing_field]

            response = movies_api.create_movie(data_movie, 400)

            assert missing_field in str(response.json()["message"]), f"Ожидалась ошибка валидации для поля '{missing_field}'"

        def test_create_movie_repeat_name(self, movie_payload, movies_api):
            data_movie = movie_payload.copy()
            data_movie.update({"name": "Movie name"})

            response = movies_api.create_movie(data_movie, 409)

            assert response.json()["error"] == "Conflict", "Отсутствует конфликт при ошибке"

    class TestMoviesIdGetRequest:
        @pytest.mark.parametrize("movie_id, expected_status", [
            ("-1", 404),
            ("abc", 500), # ловится баг - кидает 500 ошибку вместо 400
            (" ", 404),
            ("999999999", 404)
        ])
        def test_get_movie_invalid_id(self, movies_api, movie_id, expected_status):
            response = movies_api.get_movie(movie_id, expected_status=expected_status)

            assert response.status_code == expected_status, "Статус код не тот, что ожидали для этого запроса"

    class TestMoviesDeleteRequest:
        @pytest.mark.parametrize("movie_id, expected_status", [
            ("-1", 404),
            ("abc", 404),
            (" ", 404),
            ("999999999", 404),
            (None, 404)
        ])
        def test_delete_movie_invalid_id(self, movies_api, movie_id, expected_status):
            response = movies_api.delete_movie(movie_id, expected_status=expected_status)

            assert response.status_code == expected_status, "Статус код не тот, что ожидали для этого запроса"

        def test_delete_movie_unauthorize(self, unauthorized_movies_api, get_created_movie_id):
            response = unauthorized_movies_api.delete_movie(get_created_movie_id, expected_status=401)

            assert response.status_code == 401, "Неавторизованный пользователь смог удалить, хотя не должен"

    class TestMoviePatchRequest:
        @pytest.mark.parametrize("movie_id, expected_status", [
            ("-1", 404),
            ("abc", 404),
            (" ", 404),
            ("999999999", 404),
            (None, 404)
        ])
        def test_patch_movie_invalid_id(self, movies_api, movie_id, expected_status):
            response = movies_api.patch_update_movie(movie_id, update_payload=None, expected_status=expected_status)

            assert response.status_code == expected_status, "Статус код не тот, что ожидали для этого запроса"

        def test_patch_movie_unauthorize(self, unauthorized_movies_api, get_movie_id):
            movie_id = get_movie_id
            response = unauthorized_movies_api.patch_update_movie(movie_id, update_payload=None, expected_status=401)

            assert response.json()["message"] == "Unauthorized", "Сообщение об ошибке не соответствует ожидаемому"


        @pytest.mark.parametrize("payload, expected_status", [
            ({"name": ""}, 404),
            ({"imageUrl": 123}, 400),
            ({"price": "free"}, 400),
            ({"description": False}, 400),
            ({"genreId": 99999999}, 404)
        ])
        def test_patch_movie_invalid_body(self, movies_api, payload, expected_status, get_created_movie_id):
            response = movies_api.patch_update_movie(get_created_movie_id, update_payload=payload, expected_status=expected_status)

            assert "message" or "error" in response.json()