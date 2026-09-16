import pytest
import allure
from api_methods.api_user import UserAPI
from conftest import generate_unique_email, generate_unique_name


class TestUserRegistration:

    @allure.title("Создание уникального юзера - статус 200")
    @allure.description("Проверка: если создать уникального юзера - статус код 200")
    def test_create_unique_user(self, user_data):
        email, password, name = user_data
        response = UserAPI.register(email, password, name)
        assert response.status_code == 200, f"Ожидался статус 200, получен {response.status_code}"
        response_data = response.json()
        assert response_data["success"] is True
        assert "user", "accessToken" and "refreshToken" in response_data
        access_token = response_data["accessToken"]
        UserAPI.delete_user(access_token)

    @allure.title("Создание существующего юзера - статус 403")
    @allure.description("Проверка: если попытаться создать юзера с уже существующими данными- статус код 403")
    def test_create_existing_user(self, user_data):
        email, password, name = user_data
        register_response = UserAPI.register(email, password, name)
        access_token = register_response.json()["accessToken"]
        response = UserAPI.register(email, password, name)
        assert response.status_code == 403, f"Ожидался статус 403, получен {response.status_code}"
        assert response.json() == {"success":False,"message":"User already exists"}, 'Ожидался ответ {"success":False,"message":"User already exists"}'
        UserAPI.delete_user(access_token)

    @allure.title("Создание юзера без обязательного поля - статус 403")
    @allure.description("Проверка: если попытаться создать юзера без обязательного поля - статус код 403")
    def test_create_user_missing_required_field(self, user_data):
        email, password, _ = user_data
        response = UserAPI.register(email, password, name=None)
        assert response.status_code == 403, f"Ожидался статус 403, получен {response.status_code}"
        assert response.json() == {"success":False,"message":"Email, password and name are required fields"}, 'Ожидался ответ {"success":False,"message":"Email, password and name are required fields"}'


class TestUserLogin:

    @allure.title("Логин существующим юзером - статус 200")
    @allure.description("Проверка: если залогиниться корректными данными существующего юзера - статус код 200")
    def test_login_existing_user(self, user_data):
        email, password, name = user_data
        UserAPI.register(email, password, name)
        response = UserAPI.login(email, password)
        assert response.status_code == 200, f"Ожидался статус 200, получен {response.status_code}"
        response_data = response.json()
        assert response_data["success"] is True
        assert "user", "accessToken" and "refreshToken" in response_data
        access_token = response_data["accessToken"]
        UserAPI.delete_user(access_token)

    @allure.title("Логин с неправильными данными - статус 401")
    @allure.description("Проверка: попытаться залогиниться с неправильными данными - статус код 401")
    def test_login_with_invalid_credentials(self, user_data):
        email = "WrongEmail123"
        password = "WrongPassword123!"
        response = UserAPI.login(email, password)
        assert response.status_code == 401, f"Ожидался статус 401, получен {response.status_code}"
        assert response.json() == {"success":False,"message":"email or password are incorrect"}, 'Ожидался ответ {"success":False,"message":"email or password are incorrect"}'

class TestUserUpdate:

    @allure.title("Обновление имени юзера с авторизацией - статус 200")
    @allure.description("Проверка: если обновить имя юзера с авторизацией - статус код 200")
    def test_update_user_name_with_authorization(self, user_data):
        email, password, name = user_data
        new_name = generate_unique_name()
        register_response = UserAPI.register(email, password, name)
        access_token = register_response.json()["accessToken"]
        update_response = UserAPI.update_user(access_token, name=new_name)
        assert update_response.status_code == 200, f"Ожидался статус 200, получен {update_response.status_code}"
        update_data = update_response.json()
        assert update_data["success"] is True
        assert update_data["user"]["name"] == new_name
        UserAPI.delete_user(access_token)

    @allure.title("Обновление емейла юзера с авторизацией - статус 200")
    @allure.description("Проверка: если обновить емейл юзера с авторизацией - статус код 200")
    def test_update_user_email_with_authorization(self, user_data):
        email, password, name = user_data
        new_email = generate_unique_email()
        register_response = UserAPI.register(email, password, name)
        access_token = register_response.json()["accessToken"]
        update_response = UserAPI.update_user(access_token, email=new_email)
        assert update_response.status_code == 200, f"Ожидался статус 200, получен {update_response.status_code}"
        update_data = update_response.json()
        assert update_data["success"] is True
        assert update_data["user"]["email"] == new_email
        UserAPI.delete_user(access_token)

    @allure.title("Обновление имени юзера без авторизации - статус 401")
    @allure.description("Проверка: если обновить имя юзера без авторизации - статус код 401")
    def test_update_user_name_without_authorization(self, user_data):
        email, password, name = user_data
        new_name = generate_unique_name()
        register_response = UserAPI.register(email, password, name)
        access_token = register_response.json()["accessToken"]
        update_response = UserAPI.update_user(access_token=None, name=new_name)
        assert update_response.status_code == 401, f"Ожидался статус 401, получен {update_response.status_code}"
        assert update_response.json() == {"success":False,"message":"You should be authorised"}, 'Ожидался ответ {"success":False,"message":"You should be authorised"}'
        UserAPI.delete_user(access_token)

    @allure.title("Обновление емейла юзера без авторизации - статус 401")
    @allure.description("Проверка: если обновить емейл юзера без авторизации - статус код 401")
    def test_update_user_email_without_authorization(self, user_data):
        email, password, name = user_data
        new_email = generate_unique_email()
        register_response = UserAPI.register(email, password, name)
        access_token = register_response.json()["accessToken"]
        update_response = UserAPI.update_user(access_token=None, email=new_email)
        assert update_response.status_code == 401, f"Ожидался статус 401, получен {update_response.status_code}"
        assert update_response.json() == {"success":False,"message":"You should be authorised"}, 'Ожидался ответ {"success":False,"message":"You should be authorised"}'
        UserAPI.delete_user(access_token)
