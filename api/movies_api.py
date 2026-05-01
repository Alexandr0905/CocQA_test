from custom_requester.custom_requester import CustomRequest
from constants import MOVIES_ENDPOINT


class MoviesAPI(CustomRequest):

    def create_movie(self, movie_payload, expected_status=201):
        return self.send_request("POST", MOVIES_ENDPOINT, data=movie_payload, expected_status=expected_status)

    def get_movie(self, movie_id, expected_status=200):
        return self.send_request("GET", f"{MOVIES_ENDPOINT}/{movie_id}", expected_status=expected_status)

    def get_movies(self, params=None, expected_status=200):
        return self.send_request("GET", MOVIES_ENDPOINT, params=params, expected_status=expected_status)

    def put_update_movie(self, movie_id, update_payload, expected_status=200):
        return self.send_request("PUT", f"{MOVIES_ENDPOINT}/{movie_id}", data=update_payload, expected_status=expected_status)

    def patch_update_movie(self, movie_id, update_payload, expected_status=200):
        return self.send_request("PATCH", f"{MOVIES_ENDPOINT}/{movie_id}", data=update_payload, expected_status=expected_status)

    def delete_movie(self, movie_id, expected_status=200):
        return self.send_request("DELETE", f"{MOVIES_ENDPOINT}/{movie_id}", expected_status=expected_status)