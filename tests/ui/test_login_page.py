import time

import allure
import pytest
from playwright.sync_api import sync_playwright

from models.page_object_models import CinescopeLoginPage

@allure.epic("Тестирование UI")
@allure.feature("Тестирование Страницы Login")
@pytest.mark.ui
class TestloginPage:
   @allure.title("Проведение успешного входа в систему")
   def test_login_by_ui(self, registered_user):
      with sync_playwright() as playwright:
           browser = playwright.chromium.launch(headless=False)# Запуск браузера headless=False для визуального отображения
           page = browser.new_page()
           login_page = CinescopeLoginPage(page)# Создаем объект страницы Login

           login_page.login_with_workaround(registered_user.email, registered_user.password)

           login_page.assert_login_account()

           time.sleep(5)
           browser.close()