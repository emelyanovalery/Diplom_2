import requests
import allure
import urls
from data import Data

class TestUserLogin:
    @allure.title('Авторизация под зарегистрированным пользователем')
    def test_successful_login(self, create_and_delete_user):
        email, password, name, _, _ = create_and_delete_user

        login_payload = {"email": email, "password": password}
        response = requests.post(urls.BASE_URL + urls.LOGIN_ENDPOINT, json=login_payload)

        assert response.status_code == 200
        response_data = response.json()
        assert response_data["success"] is True
        assert response_data["user"]["email"] == email
        assert response_data["user"]["name"] == name
        assert "accessToken" in response_data and response_data["accessToken"].startswith("Bearer ")
        assert "refreshToken" in response_data and len(response_data["refreshToken"]) > 0

    @allure.title('Ошибка авторизации при неверном пароле')
    def test_login_with_wrong_password(self, create_and_delete_user):
        email, _, _, _, _ = create_and_delete_user

        login_payload = {"email": email, "password": "invalid_password"}
        response = requests.post(urls.BASE_URL + urls.LOGIN_ENDPOINT, json=login_payload)

        assert response.status_code == 401
        response_data = response.json()
        assert response_data["success"] is False
        assert response_data["message"] == Data.login_403_error

    @allure.title('Ошибка авторизации при некорректном email')
    def test_login_with_wrong_email(self, create_and_delete_user):
        _, password, _, _, _ = create_and_delete_user

        login_payload = {"email": "invalid_email", "password": password}
        response = requests.post(urls.BASE_URL + urls.LOGIN_ENDPOINT, json=login_payload)

        assert response.status_code == 401
        response_data = response.json()
        assert response_data["success"] is False
        assert response_data["message"] == Data.login_403_error
