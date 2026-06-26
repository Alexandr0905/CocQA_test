import time

import allure
import pytest
from playwright.sync_api import sync_playwright

from models.pages.login_page import CinescopeLoginPage
from models.pages.review_page import CinescopeReviewsPage

@allure.epic("Тестирование UI")
@allure.feature("Тестирование прикрепления отзыва к фильму")
@pytest.mark.ui
def test_leave_review(registered_user, review_data):
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False)
        page = browser.new_page()

        login_page = CinescopeLoginPage(page)
        review_page = CinescopeReviewsPage(page)

        with allure.step("Авторизация пользователя"):
            login_page.login_with_workaround(registered_user.email, registered_user.password)

        with allure.step("Переход на страницу фильма"):
            review_page.open()

        with allure.step("Оставление отзыва"):
            review_page.leave_review(review_data.text, review_data.rating)

        with allure.step("Проверка появления уведомления"):
            review_page.assert_allert_was_pop_up()

        time.sleep(5)
        browser.close()
