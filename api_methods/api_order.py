import requests
from data.config import BASE_URL, ENDPOINTS


class OrderAPI:

    @staticmethod
    def create_order(access_token, ingredients):
        payload = {"ingredients": ingredients}
        headers = {"Authorization": access_token}
        return requests.post(
            f"{BASE_URL}{ENDPOINTS['orders']}", json=payload, headers=headers
        )

    @staticmethod
    def get_user_orders(access_token):
        headers = {"Authorization": access_token}
        return requests.get(f"{BASE_URL}{ENDPOINTS['orders']}", headers=headers)
 