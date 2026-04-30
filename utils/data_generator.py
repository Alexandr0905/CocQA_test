from faker import Faker
faker = Faker()
import random
import string

class DataGenerator:

    @staticmethod
    def generate_random_email():
        return f"{faker.email()}"

    @staticmethod
    def generate_random_name():
        return f"{faker.first_name()}{faker.last_name()}"

    @staticmethod
    def generate_random_password():
        letters_upper = random.choice(string.ascii_uppercase)
        letters_lower = random.choice(string.ascii_lowercase)
        digits = random.choice(string.digits)
        special_chars = '~!?@#$%^&*_-+(){}></\\|"\'.,:'

        password = [letters_upper, letters_lower, digits]
        password_lenght = random.randint(8, 28)
        all_chars = letters_upper + letters_lower + digits + special_chars

        remaining_chars = random.choices(all_chars, k=password_lenght)
        password.extend(remaining_chars)
        random.shuffle(password)

        return "".join(password)



    @staticmethod
    def generate_film_name():
        return f"{faker.catch_phrase()}"

    @staticmethod
    def generate_film_url():
        return f"{faker.url()}"

    @staticmethod
    def generate_film_price():
        return faker.pyint()

    @staticmethod
    def generate_film_description():
        return f"{faker.text()}"

    @staticmethod
    def generate_film_location():
        return f"{faker.random_element(elements=("SPB", "MSK"))}"

    @staticmethod
    def generate_film_published():
        return faker.boolean()

    @staticmethod
    def generate_film_genre_id():
        return faker.pyint(1, 20)

    @staticmethod
    def generate_film_page_size():
        return f"{faker.pyint(1, 20)}"

    @staticmethod
    def generate_film_page_num():
        return f"{faker.pyint(1, 215)}"

    @staticmethod
    def generate_film_min_price():
        return f"{faker.pyint(1, 100)}"

    @staticmethod
    def generate_film_max_price():
        return f"{faker.pyint(500, 1000)}"

    @staticmethod
    def generate_film_created_at():
        return f"{faker.random_element(elements=("asc", "desc"))}"

    @staticmethod
    def generate_film_id():
        return faker.pyint(1, 3000)