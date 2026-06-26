from playwright.sync_api import Page
from models.pages.base_page import BasePage

class CinescopeReviewsPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.url = f"{self.home_url}movies/57169"

        self.review_input = '[data-qa-id="movie_review_input"]'
        self.rating_combobox = 'button[role="combobox"]'

        self.submit_button = '[data-qa-id="movie_review_submit_button"]'

    def open(self):
        self.open_url(self.url)

    def select_rating(self, rating: str):
        self.click_element(self.rating_combobox)
        self.page.get_by_role("option", name=rating).click()

    def leave_review(self, review: str, rating: str):
        self.enter_text_to_element(self.review_input, review)
        self.select_rating(rating)
        self.click_element(self.submit_button)

    def assert_allert_was_pop_up(self):
        self.check_pop_up_element_with_text("Отзыв успешно создан")
