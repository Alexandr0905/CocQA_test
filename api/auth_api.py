from constants import LOGIN_ENDPOINT, REGISTER_ENDPOINT, AUTH_BASE_URL
from custom_requester.custom_requester import CustomRequest

class AuthAPI(CustomRequest):
    def __init__(self, session):
        super().__init__(session=session, base_url=AUTH_BASE_URL)

    def register_user(self, user_data, expected_status=201):
        return self.send_request("POST", REGISTER_ENDPOINT, user_data, expected_status)

    def login_user(self, login_data, expected_status=200):
        return self.send_request("POST", LOGIN_ENDPOINT, login_data, expected_status)

    def authenticate(self, user_creds):
        login_data = {
            "email": user_creds[0],
            "password": user_creds[1]
        }

        response = self.login_user(login_data).json()
        if "accessToken" not in response:
            raise KeyError("token is missing")

        token = response["accessToken"]
        self._update_session_headers(**{"Authorization": "Bearer " + token})