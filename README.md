# API_AIO_TEST
Реализация тестового задания по созданию REST API сервиса с использованием
стека:
python >= 3.10
aiohttp >= 3.8
DataBase postgresql >=14
SQlAlchemy >= 2.0 CORE

## Установка и запуск

```sh
git clone https://github.com/PavelSkripov/api_aio_test.git
cd api_aio_test
make start
make migrate
make make migrate_up
make create

```
В приложении создается admin пользователь с логином login и паролем pass


## Выполненные задачи

- CRUD на таблицы Users и Roles

- Подключены сессии

- Запрос авторизации по логину и паролю

- Возможность администратору выполнять любой метод, а пользователю только со своей учетной записью

- Логирование ошибок

- Миграции через Alembic

- Docker-compose и Makefile



# Документация API


### AUTH

Авторизация

При успешной авторизации задает сессию в cookie
```sh
POST /api/v1/login
body:
{
    "login": "Oleg_5",
    "password": "123e4r5"
}
```

Создание нового пользователя (только для администраторов)

```sh
POST /api/v1/users
body:
{
    "first_name": "Надежда",
    "second_name": "Чернова",
    "login": "Nady_Chern",
    "password": "qwerty",
    "born": "1987-06-24",
    "role": "user",
}
```

### USERS

Получение всех пользователей (только для администраторов)
```sh
GET /api/v1/users/
```

Получение пользователя по ID (только для администраторов и 
пользователю по своему АКК)
```sh
GET /api/v1/users/{id}
```

Обновление пользователя (только для администраторов и 
пользователю по своему АКК)
```
PUT /api/v1/users/{id}
body:
{
    "first_name": "Надежда",
    "second_name": "Чернова",
    "login": "Nady_Chern",
    "password": "qwerty",
    "born": "1987-06-24",
}
```

Удаление пользователя (только для администраторов и 
пользователю по своему АКК)
```sh
DELETE /api/v1/users/{id}
```

### ROLES

Получение всех ролей (только для администраторов)
```sh
GET /api/v1/roles/
```

Обновление роли (только для администраторов)
```
PUT /api/v1/roles/{id}
body:
{
    "role": "user",
}
```

Удаление роли (через удаление пользователя)