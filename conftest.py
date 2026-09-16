import random
import string
import pytest


def generate_unique_email():
    random_string = "".join(random.choices(string.ascii_lowercase + string.digits, k=10))
    return f"test_{random_string}@example.com"


def generate_unique_name():
    random_string = "".join(random.choices(string.ascii_uppercase, k=5))
    return f"TestUser_{random_string}"


def generate_password():
    random_string = "".join(random.choices(string.digits, k=5))
    return f"TestPassword{random_string}"

@pytest.fixture
def user_data():
    return generate_unique_email(), generate_password(), generate_unique_name()
