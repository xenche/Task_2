import pytest
import allure
from data.config import VALID_INGREDIENTS, INVALID_INGREDIENT_HASH
from api_methods.api_order import OrderAPI


class TestCreateOrder:

    @allure.title("Создание заказа с авторизацией и ингредиентами - статус 200")
    @allure.description("Проверка: если создать заказ с валидной авторизацией и валидными ингридиентами - статус код 200")
    def test_create_order_with_authorization_with_ingredients(self, registered_user):
        email, password, name, access_token = registered_user
        response = OrderAPI.create_order(access_token, VALID_INGREDIENTS)
        assert response.status_code == 200, f"Ожидался статус 200, получен {response.status_code}"
        response_data = response.json()
        assert response_data["success"] is True

    @allure.title("Создание заказа с авторизацией без ингредиентов - статус 400")
    @allure.description("Проверка: если создать заказ с валидной авторизацией и без ингридиентов - статус код 400")
    def test_create_order_with_authorization_without_ingredients(self, registered_user):
        email, password, name, access_token = registered_user
        response = OrderAPI.create_order(access_token, ingredients=[])
        assert response.status_code == 400, f"Ожидался статус 400, получен {response.status_code}"
        assert response.json() == {"success":False,"message":"Ingredient ids must be provided"}, 'Ожидался ответ {"success":false,"message":"Ingredient ids must be provided"}'

    @allure.title("Создание заказа без авторизации - статус 200")
    @allure.description("Проверка: если создать заказ без авторизации, но с валидными ингредиентами - статус код 200")
    def test_create_order_without_authorization(self):
        response = OrderAPI.create_order(access_token=None, ingredients=VALID_INGREDIENTS)
        assert response.status_code == 200, f"Ожидался статус 200, получен {response.status_code}"
        response_data = response.json()
        assert response_data["success"] is True

    @allure.title("Создание заказа с невалидными ингредиентами - статус 500")
    @allure.description("Проверка: если создать заказ с валидной авторизацией, но с невалидными ингредиентами - статус код 500")
    def test_create_order_with_invalid_ingredient_hash(self, registered_user):
        email, password, name, access_token = registered_user
        invalid_ingredients = [INVALID_INGREDIENT_HASH]
        response = OrderAPI.create_order(access_token, invalid_ingredients)
        assert response.status_code == 500, f"Ожидался статус 500, получен {response.status_code}"


class TestGetUserOrders:
    @allure.title("Получение списка заказов с авторизацией - статус 200")
    @allure.description("Проверка: если запросить список заказов с авторизацией - статус код 200")    
    def test_get_orders_authorized_user(self, registered_user):
        email, password, name, access_token = registered_user
        response = OrderAPI.get_user_orders(access_token)
        assert response.status_code == 200, f"Ожидался статус 200, получен {response.status_code}"
        response_data = response.json()
        assert response_data["success"] is True
        assert "orders" in response_data

    @allure.title("Получение списка заказов без авторизации - статус 401")
    @allure.description("Проверка: если запросить список заказов без авторизации - статус код 401")
    def test_get_orders_unauthorized_user(self):
        response = OrderAPI.get_user_orders(access_token=None)
        assert response.status_code == 401, f"Ожидался статус 401, получен {response.status_code}"
        assert response.json() == {"success":False,"message":"You should be authorised"}, 'Ожидался ответ {"success":false,"message":"You should be authorised"}'
