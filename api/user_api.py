from custom_requester.custom_requester import CustomRequest
from constants import AUTH_BASE_URL

class UserAPI(CustomRequest):
    def __init__(self, session):
        self.session = session
        super().__init__(session=session, base_url=AUTH_BASE_URL)

    def create_user(self, user_data, expected_status=201):
        return self.send_request(
            method="POST",
            endpoint="user",
            data=user_data,
            expected_status=expected_status
        )

    def get_user(self, user_id, expected_status):
        return self.send_request("GET", f"user/{user_id}", expected_status=expected_status)

    def delete_user(self, user_id, expected_status=200):
        return self.send_request("DELETE", f"user/{user_id}", expected_status)