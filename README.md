# Автотесты API Stellar Burgers

Проект автотестов для API сервиса Stellar Burgers на Python с использованием pytest и requests.

## Структура проекта

```
.
├── conftest.py              # Фикстуры pytest и утилиты
├── requirements.txt         # Зависимости проекта
├── api_methods/             # API методы
│   ├── __init__.py
│   ├── api_user.py          # Методы для работы с пользователями
│   └── api_order.py         # Методы для работы с заказами
├── data/                    # Конфигурация
│   ├── __init__.py
│   └── config.py            # BASE_URL, эндпоинты, VALID_INGREDIENTS
└── tests/                   # Тесты
    ├── __init__.py
    ├── test_user.py         # Тесты пользователей (3 класса, 9 тестов)
    └── test_order.py        # Тесты заказов (2 класса, 6 тестов)
```

## Установка

```bash
pip install -r requirements.txt
```

## Запуск тестов

```bash
# Запустить все тесты
python -m pytest tests/ -v

# Запустить тесты пользователей
python -m pytest tests/test_user.py -v

# Запустить тесты заказов
python -m pytest tests/test_order.py -v

# Запустить конкретный тест
python -m pytest tests/test_user.py::TestUserRegistration::test_create_unique_user -v
```

## Покрытие тестами

### Тесты пользователей (`tests/test_user.py`)

| Класс | Тест | Описание |
|-------|------|----------|
| TestUserRegistration | test_create_unique_user | Создание уникального пользователя (200) |
| | test_create_existing_user | Создание существующего пользователя (403) |
| | test_create_user_missing_required_field | Создание без обязательного поля (403) |
| TestUserLogin | test_login_existing_user | Логин под существующим пользователем (200) |
| | test_login_with_invalid_credentials | Логин с неверными данными (401) |
| TestUserUpdate | test_update_user_name_with_authorization | Изменение имени с авторизацией (200) |
| | test_update_user_email_with_authorization | Изменение email с авторизацией (200) |
| | test_update_user_name_without_authorization | Изменение имени без авторизации (401) |
| | test_update_user_email_without_authorization | Изменение email без авторизации (401) |

### Тесты заказов (`tests/test_order.py`)

| Класс | Тест | Описание |
|-------|------|----------|
| TestCreateOrder | test_create_order_with_authorization_with_ingredients | Создание заказа с авторизацией и ингредиентами (200) |
| | test_create_order_with_authorization_without_ingredients | Создание заказа без ингредиентов (400) |
| | test_create_order_without_authorization | Создание заказа без авторизации |
| | test_create_order_with_invalid_ingredient_hash | Создание заказа с неверным хешем (500) |
| TestGetUserOrders | test_get_orders_authorized_user | Получение заказов авторизованным пользователем (200) |
| | test_get_orders_unauthorized_user | Получение заказов неавторизованным пользователем (401) |

## Фикстуры

- `user_data` — возвращает кортеж с уникальными данными пользователя `(email, password, name)`

## API эндпоинты

- `POST /api/auth/register` — Регистрация пользователя
- `POST /api/auth/login` — Авторизация
- `GET /api/auth/user` — Получение данных пользователя (требуется токен)
- `PATCH /api/auth/user` — Обновление данных пользователя (требуется токен)
- `DELETE /api/auth/user` — Удаление пользователя (требуется токен)
- `POST /api/orders` — Создание заказа (требуется токен)
- `GET /api/orders` — Получение заказов пользователя (требуется токен)
