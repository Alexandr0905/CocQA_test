from Cinesshop.custom_requester.custom_requester import CustomRequest

class UserAPI(CustomRequest):
    def __init__(self, session):
        super().__init__(session=session, base_url="https://auth.dev-cinescope.coconutqa.ru/")
        self.session = session

    def get_user_info(self, user_id, expected_status=200):
        return self.send_request("GET", f"user/{user_id}", expected_status)

    def delete_user(self, user_id, expected_status=200):
        return self.send_request("DELETE", f"user/{user_id}", expected_status)