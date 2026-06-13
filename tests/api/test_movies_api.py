from http.client import responses

import pytest
import allure

from conftest import common_user, admin, super_admin, get_created_movie_id
from models.base_models import MoviesListResponseModel


@allure.epic("Cinesshop movies api")
@pytest.mark.api
@pytest.mark.regression
class TestMoviesApiPositive:

    @allure.feature("Позитивные сценарии")
    @allure.title("Получение фильмов по фильтрам")
    def test_get_movies(self, movies_query_params, super_admin):
        with allure.step("Отправляем запрос на получение фильмов с параметрами"):
            response = super_admin.api.movies_api.get_movies(params=movies_query_params)

        with allure.step("Проверяем корректность поля count"):
            response_data = response.json()
            assert response_data["count"] >= 0, " Поле 'count' должно быть числом >= 0"

    @allure.feature("Позитивные сценарии")
    @allure.title("Получение фильмов без параметров")
    def test_get_movies_without_params(self, super_admin):
        with allure.step("Делаем GET-запрос на получение фильмов"):
            response = super_admin.api.movies_api.get_movies()

        with allure.step("Проверяем корректность поля count"):
            response_data = response.json()
            assert response_data["count"] >= 0, " Поле 'count' должно быть числом >= 0"

    @allure.feature("Позитивные сценарии")
    @allure.title("Создание фильма")
    @pytest.mark.smoke
    def test_create_movie(self, movie_payload, super_admin):
        with allure.step("Делаем POST-запрос на создание фильма"):
            response = super_admin.api.movies_api.create_movie(movie_payload)

        with allure.step("Переводим ответ сервера в json и вытаскиваем id созданного фильма"):
            response_data = response.json()
            movie_id = response_data["id"]

        with allure.step("Делаем GET-запрос на получение фильма по ID для последующего сравнения body"):
            get_response = super_admin.api.movies_api.get_movie(movie_id)
            get_data = get_response.json()

        with allure.step(
                "Циклом проверяем body в полученном созданном фильме и body, использованное для создания этого фильма"):
            for key in movie_payload:
                assert get_data[key] == movie_payload[
                    key], f"Несоответствие в поле '{key}'. Ожидали: {movie_payload[key]}, получили: {get_data[key]}"
            assert movie_id == get_data["id"], "ID в теле ответа не совпадает с запрошенным ID"

    @allure.feature("Позитивные сценарии")
    @allure.title("Получение фильма по id")
    def test_get_movie(self, get_created_movie_id, super_admin):
        with allure.step("Делаем GET-запрос на получение фильма по id"):
            response = super_admin.api.movies_api.get_movie(get_created_movie_id)

        with allure.step("Проверяем соответствие id фильмов"):
            assert get_created_movie_id == response.json()["id"], "ID фильмов в запросе и ответе различаются"

    @allure.feature("Позитивные сценарии")
    @allure.title("Удаление фильма по id")
    @pytest.mark.smoke
    def test_delete_movie(self, get_created_movie_id, super_admin):
        with allure.step("Делаем DELETE-запрос на удаление фильма по id"):
            response = super_admin.api.movies_api.delete_movie(get_created_movie_id)

        with allure.step("Выцепляем id фильма из ответа сервера и проверяем его с id из запроса"):
            movie_id = response.json()["id"]
            assert get_created_movie_id == movie_id, "ID фильма на удаление и непосредственно удаленного фильма не совпадают"

        with allure.step("Делаем GET-запрос чтобы убедится в том, что фильм удален"):
            super_admin.api.movies_api.get_movie(movie_id, expected_status=404)

    @allure.feature("Позитивные сценарии")
    @allure.title("Редактирование фильма")
    def test_editing_movie(self, get_created_movie_id, random_movie_price, super_admin):
        with allure.step("Создаем словарь со значением, которое хотим поменять и делаем PATCH-запрос"):
            data = {
                "price": random_movie_price
            }
            response = super_admin.api.movies_api.patch_update_movie(get_created_movie_id, data)

        with allure.step("Проверяем изменилось ли значение"):
            assert response.json()["price"] == random_movie_price, "Цена не была обновлена"

    @allure.feature("Позитивные сценарии")
    @allure.title("Изменение фильма без параметров")
    def test_patch_movie_without_params(self, super_admin, get_created_movie_id):
        with allure.step("Получаем фильм GET-запросом"):
            origin_response = super_admin.api.movies_api.get_movie(get_created_movie_id)
            origin_data = origin_response.json()

        with allure.step("Делаем PATCH-запрос на изменение фильма без передачи параметров"):
            super_admin.api.movies_api.patch_update_movie(get_created_movie_id, None)

        with allure.step("Получаем изменяемый фильм и проверяем его корректность"):
            updated_response = super_admin.api.movies_api.get_movie(get_created_movie_id)
            updated_data = updated_response.json()
            assert origin_data == updated_data, "Фильм изменился без передачи данных"

    @allure.feature("Позитивные сценарии")
    @allure.title("Получение фильмов с параметризацией")
    @pytest.mark.slow
    @pytest.mark.parametrize("minPrice, maxPrice, location , genreId", [
        (100, 500, "MSK", 2),
        (500, 800, "SPB", 1),
        (200, 500, "SPB", 4),
        (1, 300, "SPB", 5),
        (800, 1000, "MSK", 3),
    ], ids=["100 - 500 MSK 2", "500 - 800 SPB 1", "200 - 500 SPB 4", "1 - 300 SPB 5", "800 - 1000 MSK 3"])
    def test_get_movies_parametrize(self, common_user, minPrice, maxPrice, location, genreId):
        with allure.step("Создаем словарь параметров и делаем запрос на получение фильмов"):
            params = {
                "minPrice": minPrice,
                "maxPrice": maxPrice,
                "locations": location,
                "genreId": genreId,
            }
            response = common_user.api.movies_api.get_movies(params=params, expected_status=200)

        with allure.step(
                "Создаем список фильмов и циклом проверяем соответствие их параметров относительно фильтров запроса"):
            movies_list = response.json().get("movies", [])

            for movie in movies_list:
                assert minPrice <= movie["price"] <= maxPrice
                assert movie["location"] == location
                assert movie["genreId"] == genreId

    @allure.feature("Проверка прав доступа и ролевой модели")
    @pytest.mark.auth
    @pytest.mark.parametrize("user_fixture_name, expected_status_1, expected_status_2", [
        ("common_user", 403, 200),
        ("admin", 403, 200),
        ("super_admin", 200, 404)
    ])
    def test_delete_movie_role_model(self, request, user_fixture_name, get_created_movie_id, expected_status_1,
                                     expected_status_2):
        allure.dynamic.title(f"Проверка удаления фильма для роли: {user_fixture_name}")

        with allure.step(f"Инициализируем пользователя из фикстуры: {user_fixture_name}"):
            user = request.getfixturevalue(user_fixture_name)
            movie_id = get_created_movie_id

        with allure.step(f"Отправляем запрос на удаление фильма, ожидаем статус-код {expected_status_1}"):
            response = user.api.movies_api.delete_movie(movie_id, expected_status=expected_status_1)

        if response.status_code == 200:
            with allure.step("Для успешного удаления (200 OK) проверяем ID удаленного фильма"):
                deleted_movie_id = response.json()["id"]
                assert movie_id == deleted_movie_id, "ID фильма на удаление и непосредственно удаленного фильма не совпадают"

        with allure.step(f"Проверяем доступность фильма через GET-запрос, ожидаем статус-код {expected_status_2}"):
            user.api.movies_api.get_movie(movie_id, expected_status=expected_status_2)


@allure.epic("Cinesshop movies api")
@allure.feature("Негативные сценарии")
@pytest.mark.api
@pytest.mark.regression
class TestMoviesApiNegative:
    class TestMoviesPostRequest:
        @allure.title("Попытка создания фильма неавторизованным пользователем")
        @pytest.mark.auth
        def test_create_movie_unauthorized(self, movie_payload, unauthorized_api_manager):
            with allure.step("Отправляем POST запрос без авторизационного токена"):
                response = unauthorized_api_manager.movies_api.create_movie(movie_payload, expected_status=401)
                response_data = response.json()

            with allure.step("Проверяем сообщение об ошибке в ответе сервера"):
                assert response_data[
                           "message"] == "Unauthorized", f"Ожидали 'Unauthorized', получили '{response_data['message']}'"

        @allure.title("Создание фильма без передачи тела запроса (None)")
        def test_create_movie_without_params(self, movie_payload, super_admin):
            with allure.step("Отправляем POST запрос со значением тела None"):
                response = super_admin.api.movies_api.create_movie(None, expected_status=400)
                response_data = response.json()

            with allure.step("Проверяем статус Bad Request и наличие описания ошибки"):
                assert response_data["error"] == "Bad Request"
                assert "message" in response_data, "В ответе отсутствует описание ошибки (message)"

        @allure.title("Валидация типов данных: передача некорректного значения в поле")
        @pytest.mark.parametrize("field,invalid_value", [
            ("name", True),
            ("imageUrl", 2345),
            ("price", None),
            ("description", False),
            ("location", 1234),
            ("published", 1234),
            ("genreId", "1234")
        ])
        def test_create_movie_invalid_types(self, movie_payload, super_admin, field, invalid_value):
            allure.dynamic.title(f"Валидация типов: отправка некорректного значения {invalid_value} в поле {field}")

            with allure.step(f"Формируем payload с невалидным полем '{field}'"):
                data_movie = movie_payload.copy()
                data_movie.update({field: invalid_value})

            with allure.step("Отправляем POST запрос и ожидаем ошибку 400"):
                response = super_admin.api.movies_api.create_movie(data_movie, 400)
                response_data = response.json()

            with allure.step(f"Проверяем, что в тексте ошибки упоминается сбойное поле '{field}'"):
                error_message = str(response_data.get("message", "")).lower()
                assert field.lower() in error_message, f"Ожидали поле '{field}' в ошибке, но получили: {error_message}"

        @allure.title("Валидация обязательных полей: удаление поля из запроса")
        @pytest.mark.parametrize("missing_field", [
            "name", "price", "description", "location", "published", "genreId"
        ])
        def test_create_movie_missing_params(self, movie_payload, super_admin, missing_field):
            allure.dynamic.title(f"Проверка обязательности поля: удаление '{missing_field}' из запроса")

            with allure.step(f"Удаляем обязательное поле '{missing_field}' из payload"):
                data_movie = movie_payload.copy()
                del data_movie[missing_field]

            with allure.step("Отправляем POST запрос и ожидаем ошибку 400"):
                response = super_admin.api.movies_api.create_movie(data_movie, 400)

            with allure.step(f"Убеждаемся, что в сообщении валидации фигурирует пропущенное поле '{missing_field}'"):
                assert missing_field in str(
                    response.json()["message"]), f"Ожидалась ошибка валидации для поля '{missing_field}'"

        @allure.title("Попытка создания фильма с уже существующим названием (Дубликат)")
        def test_create_movie_repeat_name(self, movie_payload, super_admin):
            with allure.step("Устанавливаем дублирующее имя фильма в payload и отправляем запрос"):
                data_movie = movie_payload.copy()
                data_movie.update({"name": "Movie name"})
                response = super_admin.api.movies_api.create_movie(data_movie, 409)

            with allure.step("Проверяем наличие конфликта (Error: Conflict)"):
                assert response.json()["error"] == "Conflict", "Отсутствует конфликт при ошибке"

    class TestMoviesIdGetRequest:
        @allure.title("Запрос фильма по некорректному/несуществующему ID")
        @pytest.mark.slow
        @pytest.mark.parametrize("movie_id, expected_status", [
            ("-1", 404),
            ("abc", 500),  # Известный баг (500 вместо 400)
            (" ", 404),
            ("999999999", 404)
        ])
        def test_get_movie_invalid_id(self, super_admin, movie_id, expected_status):
            allure.dynamic.title(f"Запрос фильма по невалидному ID: '{movie_id}'")

            with allure.step(f"Отправляем GET запрос с ID '{movie_id}'"):
                response = super_admin.api.movies_api.get_movie(movie_id, expected_status=expected_status)

            with allure.step(f"Проверяем, что сервер вернул ожидаемый статус-код {expected_status}"):
                assert response.status_code == expected_status, "Статус код не тот, что ожидали для этого запроса"

    class TestMoviesDeleteRequest:
        @allure.title("Попытка удаления фильма по невалидному ID")
        @pytest.mark.slow
        @pytest.mark.parametrize("movie_id, expected_status", [
            ("-1", 404),
            ("abc", 404),
            (" ", 404),
            ("999999999", 404),
            (None, 404)
        ])
        def test_delete_movie_invalid_id(self, super_admin, movie_id, expected_status):
            allure.dynamic.title(f"Удаление фильма по невалидному ID: '{movie_id}'")

            with allure.step(f"Отправляем DELETE запрос с ID '{movie_id}'"):
                response = super_admin.api.movies_api.delete_movie(movie_id, expected_status=expected_status)

            with allure.step(f"Убеждаемся, что сервер вернул статус {expected_status}"):
                assert response.status_code == expected_status, "Статус код не тот, что ожидали для этого запроса"

        @allure.title("Попытка удаления фильма неавторизованным пользователем")
        @pytest.mark.auth
        def test_delete_movie_unauthorize(self, unauthorized_api_manager, get_created_movie_id):
            with allure.step("Отправляем DELETE запрос без авторизации"):
                response = unauthorized_api_manager.movies_api.delete_movie(get_created_movie_id, expected_status=401)

            with allure.step("Проверяем, что запрос заблокирован со статус-кодом 401"):
                assert response.status_code == 401, "Неавторизованный пользователь смог удалить, хотя не должен"

    class TestMoviePatchRequest:
        @allure.title("Попытка обновления фильма по невалидному ID")
        @pytest.mark.parametrize("movie_id, expected_status", [
            ("-1", 404),
            ("abc", 404),
            (" ", 404),
            ("999999999", 404),
            (None, 404)
        ])
        def test_patch_movie_invalid_id(self, super_admin, movie_id, expected_status):
            allure.dynamic.title(f"PATCH-обновление фильма по невалидному ID: '{movie_id}'")

            with allure.step(f"Отправляем PATCH запрос для ID '{movie_id}' без параметров"):
                response = super_admin.api.movies_api.patch_update_movie(movie_id, update_payload=None,
                                                                         expected_status=expected_status)

            with allure.step(f"Убеждаемся, что статус ответа равен {expected_status}"):
                assert response.status_code == expected_status, "Статус код не тот, что ожидали для этого запроса"

        @allure.title("Попытка обновления фильма неавторизованным пользователем")
        @pytest.mark.auth
        def test_patch_movie_unauthorize(self, unauthorized_api_manager, get_movie_id):
            with allure.step("Отправляем PATCH запрос без авторизации"):
                movie_id = get_movie_id
                response = unauthorized_api_manager.movies_api.patch_update_movie(movie_id, update_payload=None,
                                                                                  expected_status=401)

            with allure.step("Проверяем, что сервер вернул сообщение Unauthorized"):
                assert response.json()["message"] == "Unauthorized", "Сообщение об ошибке не соответствует ожидаемому"

        @allure.title("Передача невалидного тела запроса (payload) в PATCH")
        @pytest.mark.slow
        @pytest.mark.parametrize("payload, expected_status, expected_message", [
            ({"name": ""}, 400, "Некорректные данные"),
            ({"imageUrl": 123}, 400, "Поле imageUrl должно быть строкой"),
            ({"price": "free"}, 400, "Поле price должно быть числом"),
            ({"description": False}, 400, "Поле description должно быть строкой"),
            ({"genreId": 99999999}, 400, "Некорректные данные")
        ])
        def test_patch_movie_invalid_body(self, super_admin, payload, expected_status, expected_message,
                                          get_created_movie_id):
            allure.dynamic.title(f"PATCH невалидный payload: отправка {list(payload.keys())[0]}")

            with allure.step("Отправляем PATCH запрос с некорректным типом данных в теле"):
                response = super_admin.api.movies_api.patch_update_movie(get_created_movie_id, update_payload=payload,
                                                                         expected_status=expected_status)

            with allure.step(f"Проверяем, что сервер вернул ошибку, содержащую фразу: '{expected_message}'"):
                response_data = response.json()
                actual_message = response_data["message"]
                assert expected_message in actual_message, f"Ожидалось '{expected_message}', но получено '{actual_message}'"


@allure.epic("Cinesshop movies api")
@allure.feature("Интеграция с Базой Данных (DB)")
@pytest.mark.db
@pytest.mark.regression
class TestDbRequests:

    @allure.title("Проверка фильма в Базе Данных")
    def test_movie_lifecycle(self, db_helper, super_admin, movie_payload):
        with allure.step("Проверяем по БД, что фильма с таким именем еще нет в системе"):
            assert db_helper.get_movie_by_name(movie_payload["name"]) is None, "Фильм уже существует в БД до создания"

        with allure.step("Создаем фильм через отправку запроса к API"):
            response = super_admin.api.movies_api.create_movie(movie_payload)
            movie_id = response.json()["id"]

        with allure.step(f"Делаем прямой запрос в БД по ID {movie_id} и подтверждаем запись"):
            assert db_helper.get_movie_by_id(movie_id) is not None, "Фильм не появился в БД после создания через API"

        with allure.step("Удаляем фильм через вызов API"):
            super_admin.api.movies_api.delete_movie(movie_id)

        with allure.step("Проверяем прямым запросом в БД, что запись о фильме успешно удалена"):
            assert db_helper.get_movie_by_id(movie_id) is None, "Фильм не удалился из БД после удаления через API"