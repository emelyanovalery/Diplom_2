import requests
import allure
import urls
from data import Data
from helper import Generator


class TestRegistration:

    @allure.title('Проверка успешной регистрации пользователя с заполнением всех обязательных полей')
    def test_successful_registration(self, create_and_delete_user):
        email, _, name, response_create_user, _ = create_and_delete_user

        assert response_create_user.status_code == 200, response_create_user.text
        response_data = response_create_user.json()

        assert response_data.get("success") is True
        assert response_data["user"]["email"] == email
        assert response_data["user"]["name"] == name
        assert isinstance(response_data.get("accessToken"), str) and response_data["accessToken"].startswith("Bearer ")
        assert isinstance(response_data.get("refreshToken"), str) and len(response_data["refreshToken"]) > 0

    @allure.title('Проверка ошибки при регистрации без указания пароля')
    def test_registration_without_password(self):
        payload = {
            "email": Generator.fake_email(),
            "password": "",
            "name": Generator.fake_name()
        }
        response = requests.post(urls.BASE_URL + urls.REGISTRATION_ENDPOINT, json=payload)

        assert response.status_code == 403, response.text
        response_data = response.json()

        assert response_data.get("success") is False
        assert response_data.get("message") == Data.registration_data_403_error

    @allure.title('Проверка ошибки при регистрации пользователя с уже существующими данными')
    def test_registration_existing_user(self, create_and_delete_user):
        email, password, name, _, _ = create_and_delete_user

        payload = {
            "email": email,
            "password": password,
            "name": name
        }
        response = requests.post(urls.BASE_URL + urls.REGISTRATION_ENDPOINT, json=payload)

        assert response.status_code == 403, response.text
        response_data = response.json()

        assert response_data.get("success") is False
        assert response_data.get("message") == Data.registration_user_403_error
