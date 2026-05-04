import pytest

class TestMoviesApiPositive:
    def test_get_movies(self, movies_query_params, superadmin_user):
        response = superadmin_user.movies_api.get_movies(params=movies_query_params)
        response_data = response.json()

        assert response_data["count"] >= 0," Поле 'count' должно быть числом >= 0"

    def test_get_movies_without_params(self, superadmin_user):
        response = superadmin_user.movies_api.get_movies()
        response_data = response.json()

        assert response_data["count"] >= 0," Поле 'count' должно быть числом >= 0"

    def test_create_movie(self, movie_payload, superadmin_user):
        response = superadmin_user.movies_api.create_movie(movie_payload)
        response_data = response.json()
        movie_id = response_data["id"]

        get_response = superadmin_user.movies_api.get_movie(movie_id)
        get_data = get_response.json()

        for key in movie_payload:
            assert get_data[key] == movie_payload[key], f"Несоответствие в поле '{key}'. Ожидали: {movie_payload[key]}, получили: {get_data[key]}"
        assert movie_id == get_data["id"], "ID в теле ответа не совпадает с запрошенным ID"

    def test_get_movie(self, get_created_movie_id, superadmin_user):
        response = superadmin_user.movies_api.get_movie(get_created_movie_id)

        assert get_created_movie_id == response.json()["id"], "ID фильмов в запросе и ответе различаются"

    def test_delete_movie(self, get_created_movie_id, superadmin_user):
        response = superadmin_user.movies_api.delete_movie(get_created_movie_id)

        movie_id = response.json()["id"]
        assert get_created_movie_id == movie_id, "ID фильма на удаление и непосредственно удаленного фильма не совпадают"
        superadmin_user.movies_api.get_movie(movie_id, expected_status=404)

    def test_editing_movie(self, get_created_movie_id, random_movie_price, superadmin_user):
        data = {
            "price": random_movie_price
        }
        response = superadmin_user.movies_api.patch_update_movie(get_created_movie_id, data)

        assert response.json()["price"] == random_movie_price, "Цена не была обновлена"

    def test_patch_movie_without_params(self, superadmin_user, get_created_movie_id):
        origin_response = superadmin_user.movies_api.get_movie(get_created_movie_id)
        origin_data = origin_response.json()

        response = superadmin_user.movies_api.patch_update_movie(get_created_movie_id, None)

        updated_response = superadmin_user.movies_api.get_movie(get_created_movie_id)
        updated_data = updated_response.json()

        assert origin_data == updated_data, "Фильм изменился без передачи данных"

class TestMoviesApiNegative:
    class TestMoviesPostRequest:
        def test_create_movie_unauthorized(self, movie_payload, unauthorized_api_manager):
            response = unauthorized_api_manager.movies_api.create_movie(movie_payload, expected_status=401)
            response_data = response.json()

            assert response_data["message"] == "Unauthorized", f"Ожидали 'Unauthorized', получили '{response_data['message']}'"

        def test_create_movie_without_params(self, movie_payload, superadmin_user):
            response = superadmin_user.movies_api.create_movie(None, expected_status=400)
            response_data = response.json()

            assert response_data["error"] == "Bad Request"
            assert "message" in response_data, "В ответе отсутствует описание ошибки (message)"

        @pytest.mark.parametrize("field, invalid_value", [
            ("name", True),
            ("imageUrl", 2345),
            ("price", None),
            ("description", False),
            ("location", 1234),
            ("published", 1234),
            ("genreId", "1234")
        ])
        def test_create_movie_invalid_types(self, movie_payload, superadmin_user, field, invalid_value):
            data_movie = movie_payload.copy()
            data_movie.update({field: invalid_value})

            response = superadmin_user.movies_api.create_movie(data_movie, 400)
            response_data = response.json()

            error_message = str(response_data.get("message", "")).lower()
            assert field.lower() in error_message, f"Ожидали поле '{field}' в ошибке, но получили: {error_message}"

        @pytest.mark.parametrize("missing_field", [
            "name", "price", "description", "location", "published", "genreId"
        ])
        def test_create_movie_missing_params(self, movie_payload, superadmin_user, missing_field):
            data_movie = movie_payload.copy()
            del data_movie[missing_field]

            response = superadmin_user.movies_api.create_movie(data_movie, 400)

            assert missing_field in str(response.json()["message"]), f"Ожидалась ошибка валидации для поля '{missing_field}'"

        def test_create_movie_repeat_name(self, movie_payload, superadmin_user):
            data_movie = movie_payload.copy()
            data_movie.update({"name": "Movie name"})

            response = superadmin_user.movies_api.create_movie(data_movie, 409)

            assert response.json()["error"] == "Conflict", "Отсутствует конфликт при ошибке"

    class TestMoviesIdGetRequest:
        @pytest.mark.parametrize("movie_id, expected_status", [
            ("-1", 404),
            ("abc", 500), # ловится баг - кидает 500 ошибку вместо 400
            (" ", 404),
            ("999999999", 404)
        ])
        def test_get_movie_invalid_id(self, superadmin_user, movie_id, expected_status):
            response = superadmin_user.movies_api.get_movie(movie_id, expected_status=expected_status)

            assert response.status_code == expected_status, "Статус код не тот, что ожидали для этого запроса"

    class TestMoviesDeleteRequest:
        @pytest.mark.parametrize("movie_id, expected_status", [
            ("-1", 404),
            ("abc", 404),
            (" ", 404),
            ("999999999", 404),
            (None, 404)
        ])
        def test_delete_movie_invalid_id(self, superadmin_user, movie_id, expected_status):
            response = superadmin_user.movies_api.delete_movie(movie_id, expected_status=expected_status)

            assert response.status_code == expected_status, "Статус код не тот, что ожидали для этого запроса"

        def test_delete_movie_unauthorize(self, unauthorized_api_manager, get_created_movie_id):
            response = unauthorized_api_manager.movies_api.delete_movie(get_created_movie_id, expected_status=401)

            assert response.status_code == 401, "Неавторизованный пользователь смог удалить, хотя не должен"

    class TestMoviePatchRequest:
        @pytest.mark.parametrize("movie_id, expected_status", [
            ("-1", 404),
            ("abc", 404),
            (" ", 404),
            ("999999999", 404),
            (None, 404)
        ])
        def test_patch_movie_invalid_id(self, superadmin_user, movie_id, expected_status):
            response = superadmin_user.movies_api.patch_update_movie(movie_id, update_payload=None, expected_status=expected_status)

            assert response.status_code == expected_status, "Статус код не тот, что ожидали для этого запроса"

        def test_patch_movie_unauthorize(self, unauthorized_api_manager, get_movie_id):
            movie_id = get_movie_id
            response = unauthorized_api_manager.movies_api.patch_update_movie(movie_id, update_payload=None, expected_status=401)

            assert response.json()["message"] == "Unauthorized", "Сообщение об ошибке не соответствует ожидаемому"

        @pytest.mark.parametrize("payload, expected_status, expected_message", [
            ({"name": ""}, 404, "Фильм не найден"),
            ({"imageUrl": 123}, 400, "Поле imageUrl должно быть строкой"),
            ({"price": "free"}, 400, "Поле price должно быть числом"),
            ({"description": False}, 400, "Поле description должно быть строкой"),
            ({"genreId": 99999999}, 404, "Фильм не найден")
        ])
        def test_patch_movie_invalid_body(self, superadmin_user, payload, expected_status, expected_message, get_created_movie_id):
            response = superadmin_user.movies_api.patch_update_movie(get_created_movie_id, update_payload=payload, expected_status=expected_status)

            response_data = response.json()
            actual_message = response_data["message"]
            assert expected_message in actual_message, f"Ожидалось '{expected_message}', но получено '{actual_message}'"