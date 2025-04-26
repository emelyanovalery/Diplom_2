import requests
import allure
import urls
from data import Data

class TestOrderCreation:
    @allure.title('Создание заказа с ингредиентами без авторизации')
    def test_create_order_with_ingredients_no_auth(self):
        order_payload = {"ingredients": [Data.ingredient_1_id, Data.ingredient_2_id]}
        response = requests.post(urls.BASE_URL + urls.ORDER_ENDPOINT, json=order_payload)

        assert response.status_code == 200
        response_data = response.json()
        assert response_data["success"] is True
        assert response_data["name"] == Data.order_name
        assert "order" in response_data and isinstance(response_data["order"]["number"], int)

    @allure.title('Создание заказа без ингредиентов без авторизации')
    def test_create_order_without_ingredients_no_auth(self):
        order_payload = {}
        response = requests.post(urls.BASE_URL + urls.ORDER_ENDPOINT, json=order_payload)

        assert response.status_code == 400
        response_data = response.json()
        assert response_data["success"] is False
        assert response_data["message"] == Data.ingredients_error

    @allure.title('Создание заказа с некорректными ингредиентами без авторизации')
    def test_create_order_invalid_ingredients_no_auth(self):
        order_payload = {"ingredients": ["1", ""]}
        response = requests.post(urls.BASE_URL + urls.ORDER_ENDPOINT, json=order_payload)

        assert response.status_code == 500
        assert "Internal Server Error" in response.text

    @allure.title('Создание заказа с ингредиентами с авторизацией')
    def test_create_order_with_ingredients_with_auth(self, create_and_delete_user):
        email, _, name, _, token = create_and_delete_user
        order_payload = {"ingredients": [Data.ingredient_1_id, Data.ingredient_2_id]}
        response = requests.post(urls.BASE_URL + urls.ORDER_ENDPOINT, json=order_payload, headers=token)

        assert response.status_code == 200
        response_data = response.json()
        assert response_data["success"] is True
        assert response_data["name"] == Data.order_name

        order_info = response_data["order"]
        ingredients = order_info["ingredients"]
        assert len(ingredients) == 2
        assert ingredients[0] == Data.ingredient_1
        assert ingredients[1] == Data.ingredient_2

        assert isinstance(order_info["_id"], str)

        owner_info = order_info["owner"]
        assert owner_info["name"] == name
        assert owner_info["email"] == email
        assert isinstance(owner_info["createdAt"], str)
        assert isinstance(owner_info["updatedAt"], str)

        assert order_info["status"] == "done"
        assert order_info["name"] == Data.order_name
        assert isinstance(order_info["number"], int) and order_info["number"] > 0
        assert isinstance(order_info["price"], int) and order_info["price"] > 0
        assert isinstance(order_info["createdAt"], str)
        assert isinstance(order_info["updatedAt"], str)

    @allure.title('Создание заказа без ингредиентов с авторизацией')
    def test_create_order_without_ingredients_with_auth(self, create_and_delete_user):
        _, _, _, _, token = create_and_delete_user
        order_payload = {}
        response = requests.post(urls.BASE_URL + urls.ORDER_ENDPOINT, json=order_payload, headers=token)

        assert response.status_code == 400
        response_data = response.json()
        assert response_data["success"] is False
        assert response_data["message"] == Data.ingredients_error

    @allure.title('Создание заказа с неверными ингредиентами с авторизацией')
    def test_create_order_invalid_ingredients_with_auth(self, create_and_delete_user):
        _, _, _, _, token = create_and_delete_user
        order_payload = {"ingredients": ["1", ""]}
        response = requests.post(urls.BASE_URL + urls.ORDER_ENDPOINT, json=order_payload, headers=token)

        assert response.status_code == 500
        assert "Internal Server Error" in response.text

class TestRetrieveOrders:
    @allure.title('Получение списка заказов без авторизации')
    def test_get_orders_no_auth(self):
        response = requests.get(urls.BASE_URL + urls.ORDER_ENDPOINT)

        assert response.status_code == 401
        response_data = response.json()
        assert response_data["success"] is False
        assert response_data["message"] == Data.get_orders_401_error

    @allure.title('Получение списка заказов с авторизацией')
    def test_get_orders_with_auth(self, create_and_delete_user):
        email, _, name, _, token = create_and_delete_user
        order_payload = {"ingredients": [Data.ingredient_1_id, Data.ingredient_2_id]}
        create_order_response = requests.post(urls.BASE_URL + urls.ORDER_ENDPOINT, json=order_payload, headers=token)

        assert create_order_response.status_code == 200
        order_data = create_order_response.json()
        assert order_data["success"] is True
        assert order_data["name"] == Data.order_name

        order_info = order_data["order"]
        ingredients = order_info["ingredients"]
        assert len(ingredients) == 2
        assert ingredients[0] == Data.ingredient_1
        assert ingredients[1] == Data.ingredient_2
        assert isinstance(order_info["_id"], str)

        owner_info = order_info["owner"]
        assert owner_info["name"] == name
        assert owner_info["email"] == email
        assert isinstance(owner_info["createdAt"], str)
        assert isinstance(owner_info["updatedAt"], str)

        assert order_info["status"] == "done"
        assert order_info["name"] == Data.order_name
        assert isinstance(order_info["number"], int) and order_info["number"] > 0
        assert isinstance(order_info["price"], int) and order_info["price"] > 0
        assert isinstance(order_info["createdAt"], str)
        assert isinstance(order_info["updatedAt"], str)

        get_orders_response = requests.get(urls.BASE_URL + urls.ORDER_ENDPOINT, headers=token)

        assert get_orders_response.status_code == 200
        orders_data = get_orders_response.json()
        assert orders_data["success"] is True

        assert isinstance(orders_data["orders"], list) and len(orders_data["orders"]) == 1
        fetched_order = orders_data["orders"][0]
        assert "_id" in fetched_order and isinstance(fetched_order["_id"], str)
        assert fetched_order["ingredients"] == [Data.ingredient_1_id, Data.ingredient_2_id]
        assert fetched_order["status"] == "done"
        assert fetched_order["name"] == Data.order_name
        assert isinstance(fetched_order["createdAt"], str)
        assert isinstance(fetched_order["updatedAt"], str)
        assert isinstance(fetched_order["number"], int) and fetched_order["number"] > 0

        assert isinstance(orders_data["total"], int) and orders_data["total"] >= 0
        assert isinstance(orders_data["totalToday"], int) and orders_data["totalToday"] >= 0
