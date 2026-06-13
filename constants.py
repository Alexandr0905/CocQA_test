from enum import Enum

AUTH_BASE_URL = "https://auth.dev-cinescope.coconutqa.ru/"
API_BASE_URL = "https://api.dev-cinescope.coconutqa.ru/"

HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json"
}

LOGIN_ENDPOINT = "/login"
REGISTER_ENDPOINT = "/register"
MOVIES_ENDPOINT = "/movies"

RED = '\033[31m'
GREEN = '\033[32m'
RESET = '\033[0m'

class Roles(Enum):
    USER = "USER"
    ADMIN = "ADMIN"
    SUPER_ADMIN = "SUPER_ADMIN"

class City(Enum):
    MSK = "MSK"
    SPB = "SPB"