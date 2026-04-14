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
        password_lenght = random.randint(8, 30)
        all_chars = letters_upper + letters_lower + digits + special_chars

        remaining_chars = random.choices(all_chars, k=password_lenght)
        password.extend(remaining_chars)
        random.shuffle(password)

        return "".join(password)