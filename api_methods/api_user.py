import requests
from data.config import BASE_URL, ENDPOINTS


class UserAPI:
    @staticmethod
    def register(email, password, name):
        payload = {"email": email, "password": password, "name": name}
        return requests.post(f"{BASE_URL}{ENDPOINTS['register']}", json=payload)

    @staticmethod
    def login(email, password):
        payload = {"email": email, "password": password}
        return requests.post(f"{BASE_URL}{ENDPOINTS['login']}", json=payload)

    @staticmethod
    def update_user(access_token, email=None, name=None):
        payload = {}
        if email:
            payload["email"] = email
        if name:
            payload["name"] = name
        headers = {"Authorization": access_token}
        return requests.patch(
            f"{BASE_URL}{ENDPOINTS['user']}", json=payload, headers=headers
        )

    @staticmethod
    def delete_user(access_token):
        headers = {"Authorization": access_token}
        return requests.delete(f"{BASE_URL}{ENDPOINTS['user']}", headers=headers)
