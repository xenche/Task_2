import pytest
from utils.helpers import generate_user_data
from api_methods.api_user import UserAPI


@pytest.fixture
def registered_user():
    email, password, name = generate_user_data()
    register_response = UserAPI.register(email, password, name)
    access_token = register_response.json()["accessToken"]
    yield email, password, name, access_token
    UserAPI.delete_user(access_token)
