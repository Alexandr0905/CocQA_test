from api.api_manager import ApiManager
from constants import Roles


class User:
    def __init__(self, email: str, password: str, roles: list[Roles], api: ApiManager):
        self.email = email
        self.password = password
        self.roles = roles
        self.api = api

    @property
    def creds(self):
        return self.email, self.password