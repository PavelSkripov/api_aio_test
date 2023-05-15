from urllib.request import Request
from aiohttp import web
from aiohttp.web_exceptions import HTTPUnauthorized, HTTPBadRequest
from aiohttp_session import (get_session, setup as setup_aiohttp_session,
                             SimpleCookieStorage)
import datetime
import logging


# получение пользовательского логгера и установка уровня логирования
logger = logging.getLogger('app.views')
logger.setLevel(logging.INFO)
# настройка обработчика и форматировщика
handler = logging.FileHandler("py_log.log", mode='w')
# вывод в консоль
console_out = logging.StreamHandler()
formatter = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")
# добавление форматировщика к обработчику
handler.setFormatter(formatter)
# добавление обработчика к логгеру
logger.addHandler(handler)
logger.addHandler(console_out)


class AuthView(web.View):
    """метод авторизации"""

    async def post(self):
        data = await self.request.json()
        logger.info(f'AuthView: пользователь логинится с данными {data}')
        result = await self.request.app['db'].fetchrow(
            'SELECT * FROM Users WHERE login = $1 AND password = $2',
            data['login'],
            data['password'],
            )
        if result is not None:
            # создаем новую сессию
            session = await get_session(self.request)
            # дополняем данными
            session['user'] = {
                'login': data['login'],
                'last_login': datetime.datetime.now().isoformat(),
                'role': str(result[7]),
                'id': result[0],
                }
            logger.info(f"AuthView: объект пользователя: {session['user']=}")
            # отдаем успешный ответ с этой сессией
            return web.Response(text='Пользователь авторизован')
        else:
            return web.Response(text='Пользователь не найден')


async def access_check(request: Request) -> str | int | HTTPUnauthorized:
    """
        Функция извлекает данные сессии и проверяет роль авторизованного
        пользователя. В случае отсутствия данных в сессии возвращает
        HTTPUnauthorized.

        :param request: объект request, получаемый от клиента
        :type request: Request
        :return: возвращает роль 'admin', либо id юзера, либо HTTPUnauthorized
    """
    session = await get_session(request)
    if session.new:
        logger.info('SecuredView: Пользователь не авторизован, отдаю 401')
        raise HTTPUnauthorized(reason='Нет авторизации')
    if session['user']['role'] == 'admin':
        return 'admin'
    else:
        return session['user']['id']


async def get_list_users(request: Request) -> web.Response:
    """
        Функция выдает администратору весь список объектов Users.

        :param request: объект request, получаемый от клиента
        :type request: Request
        :return: возвращает список объектов Users, либо 'Доступ запрещен'
    """
    check = await access_check(request)
    # можно получить данные из сессии как из словаря
    if check == 'admin':
        logger.info("GET /api/v1/users получение списка объектов Users")
        result = await request.app['db'].fetch('SELECT * FROM Users')
        records = [dict(q) for q in result]
        return web.Response(text=str(records))
    else:
        return web.Response(text='Доступ запрещен')


async def get_user(request: Request) -> web.Response:
    """
        Функция выдает администратору и пользователю объект Users по id.
        Пользователю только по своему id.

        :param request: объект request, получаемый от клиента
        :type request: Request
        :return: возвращает объект Users, либо 'Доступ запрещен'
    """
    user_id = int(request.match_info.get('id', 1))
    check = await access_check(request)
    if check != 'admin' and check != user_id:
        return web.Response(text='Доступ запрещен')
    else:
        result = await request.app['db'].fetch(
            'SELECT * FROM Users WHERE id = $1', user_id
            )
        logger.info("GET /api/v1/users/id получение объекта Users по id")
        records = [dict(q) for q in result]
        return web.Response(text=str(records))


async def create_user(request: Request) -> web.HTTPOk | web.Response:
    """
        Функция создает объект Users, доступна только администратору.

        :param request: объект request, получаемый от клиента
        :type request: Request
        :return: возвращает статус ОК (200), либо 'Доступ запрещен'
    """
    check = await access_check(request)
    if check == 'admin':
        data = await request.json()
        logger.info(f"data === {data}")
        if data['role'] == 'admin' or data['role'] == 'user':
            try:
                result = await request.app['db'].fetchrow(
                    "INSERT into Users(first_name, last_name, login,\
                        password, birthday, registration_date, role)\
                            values ($1, $2, $3, $4, $5, $6, $7) returning id",
                    data['first_name'],
                    data['last_name'],
                    data['login'],
                    data['password'],
                    datetime.date.fromisoformat(data['birthday']),
                    datetime.datetime.now(),
                    data['role'],
                    )
            except KeyError:
                logger.exception("KeyError")
                raise HTTPBadRequest(reason='Некорректные данные пользователя')
            return_id = int(result[0])
            logger.info("POST /api/v1/users создание объекта Users")
            return await create_role(request, return_id, data['role'])
        else:
            return web.Response(text='Доступны только роли admin или user')
    else:
        return web.Response(text='Доступ запрещен')


async def create_role(request: Request, user_id: int, role: str) -> web.HTTPOk:
    """
        Функция создает объект Roles, доступна только администратору.

        :param request: объект request, получаемый от клиента
        :type request: Request
        :param user_id: id последнего созданного объекта Users
        :type user_id: int
        :param role: роль пользователя
        :type role: str
        :return: возвращает статус ОК (200)'
    """
    await request.app['db'].fetchrow(
        "INSERT into Roles(role, users_id) values ($1, $2) returning *",
        role,
        user_id,
        )
    logger.info("create_role создание объекта в таблице Roles")
    return web.HTTPOk()


async def delete_user(request: Request) -> web.Response | web.HTTPOk:
    """
        Функция удаляет объект Users, доступна администратору и пользователю,
        но пользователю только для своего АКК.

        :param request: объект request, получаемый от клиента
        :type request: Request
        :return: возвращает статус ОК (200), либо 'Доступ запрещен'
    """
    check = await access_check(request)
    user_id = int(request.match_info.get('id'))
    if check != 'admin' and check != user_id:
        return web.Response(text='Доступ запрещен')
    else:
        await request.app['db'].execute(
            'DELETE FROM Users WHERE id = $1', user_id
            )
        logger.info("DELETE /api/v1/users/id удаление объекта Users по id")
        return await delete_role(request)


async def delete_role(request: Request) -> web.HTTPOk:
    """
        Функция удаляет объект Roles.

        :param request: объект request, получаемый от клиента
        :type request: Request
        :return: возвращает статус ОК (200)
    """
    user_id = int(request.match_info.get('id'))
    await request.app['db'].execute(
        'DELETE FROM Roles WHERE id = $1', user_id
        )
    logger.info("Удаление объекта Roles по id")
    return web.HTTPOk()


async def update_user(request: Request) -> web.Response | web.HTTPOk:
    """
        Функция обновляет объект Users, доступна только администратору и
        пользователю, но пользователю только для своего АКК.

        :param request: объект request, получаемый от клиента
        :type request: Request
        :return: возвращает статус ОК (200), либо 'Доступ запрещен'
    """
    check = await access_check(request)
    user_id = int(request.match_info.get('id'))
    if check != 'admin' and check != user_id:
        return web.Response(text='Доступ запрещен')
    else:
        data = await request.json()
        logger.info(f"data === {data}")
        try:
            await request.app['db'].fetchrow(
                "UPDATE Users set first_name = $1, last_name = $2, login = $3,\
                    password = $4, birthday = $5, registration_date = $6\
                        WHERE id = $7 returning *",
                data['first_name'],
                data['last_name'],
                data['login'],
                data['password'],
                datetime.date.fromisoformat(data['birthday']),
                datetime.datetime.now(),
                user_id,
                )
        except KeyError:
            logger.exception("KeyError")
            raise HTTPBadRequest(reason='Некорректные данные пользователя')
        logger.info("PUT /api/v1/users/id обновление объекта Users по id")
        return web.HTTPOk()


async def update_role(request: Request) -> web.Response | web.HTTPOk:
    """
        Функция обновляет объект Roles, доступна только администратору.

        :param request: объект request, получаемый от клиента
        :type request: Request
        :return: возвращает статус ОК (200), либо 'Доступ запрещен'
    """
    check = await access_check(request)
    if check == 'admin':
        data = await request.json()
        logger.info(f"data === {data}")
        if data['role'] == 'admin' or data['role'] == 'user':
            user_id = int(request.match_info.get('id'))
            await request.app['db'].fetchrow(
                "UPDATE Roles set role = $1 WHERE users_id = $2 returning *",
                data['role'],
                user_id,
                )
            logger.info("PUT /api/v1/roles/id обновление объекта Roles по id")
            return await update_user_role(request, user_id, data['role'])
        else:
            return web.Response(text='Доступны только роли admin или user')
    else:
        return web.Response(text='Доступ запрещен')


async def update_user_role(
        request: Request, user_id: int, role: str
        ) -> web.HTTPOk:
    """
        Функция обновляет отдельно роль в объекте User.

        :param request: объект request, получаемый от клиента
        :type request: Request
        :param user_id: id объекта Users
        :type user_id: int
        :param role: роль пользователя
        :type role: str
        :return: возвращает статус ОК (200)
    """
    data = await request.json()
    logger.info(f"data === {data}")
    user_id = int(request.match_info.get('id'))
    await request.app['db'].fetchrow(
        "UPDATE Users set role = $1 WHERE id = $2 returning *",
        role,
        user_id,
        )
    logger.info("Обновление role в Users по id")
    return web.HTTPOk()


async def get_list_roles(request: Request) -> web.Response:
    """
        Функция выдает администратору весь список объектов Roles.

        :param request: объект request, получаемый от клиента
        :type request: Request
        :return: возвращает список объектов Roles, либо 'Доступ запрещен'
    """
    check = await access_check(request)
    if check == 'admin':
        result = await request.app['db'].fetch('SELECT * FROM Roles')
        records = [dict(q) for q in result]
        logger.info("GET /api/v1/roles получение списка объектов Roles")
        return web.Response(text=str(records))
    else:
        return web.Response(text='Доступ запрещен')


def setup_cookie(app: web.Application):
    """
        Функция создает cookie сессии. Данные сессии в незашифрованном виде.

        :param app: объект Application
        :type app: Application
    """
    setup_aiohttp_session(app, SimpleCookieStorage())
