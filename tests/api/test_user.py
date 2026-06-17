import pytest
from models.base_models import RegisterUserResponse

class TestUser:

    def test_create_user(self, super_admin, creation_user_data):
        response = super_admin.api.user_api.create_user(creation_user_data)
        response_data = RegisterUserResponse(**response.json())

        assert response_data.email == creation_user_data.email
        assert response_data.fullName == creation_user_data.fullName
        assert response_data.roles == creation_user_data.roles
        assert response_data.verified is True

    def test_get_user_by_locator(self, super_admin, creation_user_data):
        created_user = RegisterUserResponse(**super_admin.api.user_api.create_user(creation_user_data).json())
        response_by_id = RegisterUserResponse(**super_admin.api.user_api.get_user(created_user.id, expected_status=200).json())
        response_by_email = RegisterUserResponse(**super_admin.api.user_api.get_user(creation_user_data.email, expected_status=200).json())

        assert response_by_id == response_by_email, "Содержание ответов должно быть идентичным"

    @pytest.mark.slow
    def test_get_user_by_id_common_user(self, common_user):
        common_user.api.user_api.get_user(common_user.email, expected_status=403)
