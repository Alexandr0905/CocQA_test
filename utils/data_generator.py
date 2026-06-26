import datetime
from datetime import datetime

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

        special_chars = '?@#$%^&*_-+()[]{}'
        password = [letters_upper, letters_lower, digits]

        total_length = random.randint(8, 20)
        remaining_length = total_length - len(password)

        all_chars = string.ascii_letters + string.digits + special_chars

        remaining_chars = random.choices(all_chars, k=remaining_length)
        password.extend(remaining_chars)

        random.shuffle(password)

        return "".join(password)

    @staticmethod
    def generate_film_id():
        return faker.pyint(2000, 3000)

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
        return f"{faker.pyint(1, 5)}"

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
    def generate_film_created_at_data() -> str:
        from datetime import datetime
        return datetime.now().isoformat()

    @staticmethod
    def generate_user_data() -> dict:
        from uuid import uuid4

        return {
            'id': f'{uuid4()}',  # генерируем UUID как строку
            'email': DataGenerator.generate_random_email(),
            'full_name': DataGenerator.generate_random_name(),
            'password': DataGenerator.generate_random_password(),
            'created_at': datetime.datetime.now(),
            'updated_at': datetime.datetime.now(),
            'verified': False,
            'banned': False,
            'roles': '{USER}'
        }

    @staticmethod
    def generate_movie_data() -> dict:

        return {
            # 'id': DataGenerator.generate_film_id(),
            'name': DataGenerator.generate_film_name(),
            'price': DataGenerator.generate_film_price(),
            'description': DataGenerator.generate_film_description(),
            'image_url': DataGenerator.generate_film_url(),
            'location': DataGenerator.generate_film_location(),
            'published': DataGenerator.generate_film_published(),
            'rating': 4.55,
            'genre_id': DataGenerator.generate_film_genre_id(),
            'created_at': DataGenerator.generate_film_created_at_data()
        }

    @staticmethod
    def generate_review_description():
        return f"{faker.text()}"

    @staticmethod
    def generate_review_rating():
        return str(faker.pyint(1, 5))