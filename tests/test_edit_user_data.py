import requests
import allure
import urls
from data import Data
from helper import Generator

class TestUpdateUserInfo:
    @allure.title('Изменение профиля — пользователь авторизован')
    def test_update_profile_with_auth(self, create_and_delete_user):
        _, _, _, _, token = create_and_delete_user

        updated_email = Generator.fake_email()
        updated_name = Generator.fake_name()
        update_payload = {"email": updated_email, "name": updated_name}
        response = requests.patch(urls.BASE_URL + urls.USER_ENDPOINT, json=update_payload, headers=token)

        assert response.status_code == 200
        response_data = response.json()
        assert response_data["success"] is True
        assert response_data["user"]["email"] == updated_email
        assert response_data["user"]["name"] == updated_name

    @allure.title('Изменение профиля — пользователь без авторизации')
    def test_update_profile_without_auth(self):
        update_payload = {"email": Generator.fake_email(), "name": Generator.fake_name()}
        response = requests.patch(urls.BASE_URL + urls.USER_ENDPOINT, json=update_payload)

        assert response.status_code == 401
        response_data = response.json()
        assert response_data["success"] is False
        assert response_data["message"] == Data.edit_data_401_error
