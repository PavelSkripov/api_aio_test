import asyncpg
from aiohttp import web
import logging
# получение пользовательского логгера и установка уровня логирования
logger = logging.getLogger('app.accessor')
logger.setLevel(logging.INFO)

# настройка обработчика и форматировщика в соответствии с нашими нуждами
handler = logging.FileHandler("py_log.log", mode='w')
# вывод в консоль
console_out = logging.StreamHandler()
formatter = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")

# добавление форматировщика к обработчику
handler.setFormatter(formatter)
# добавление обработчика к логгеру
logger.addHandler(handler)


async def pg_context(app: web.Application):
    """
        Функция осуществляет подключение к базе данных.

        :param app: объект Application
        :type app: Application
    """
    conf = app['config']['postgres']
    try:
        engine = await asyncpg.connect(
            host=conf['host'],
            port=conf['port'],
            user=conf['user'],
            password=conf['password'],
            database=conf['database'],
        )
        app['db'] = engine
        logger.info(f"app['db'] = {app['db']}")
    except (asyncpg.exceptions.InvalidCatalogNameError,
            asyncpg.CannotConnectNowError,
            asyncpg.PostgresConnectionError):
        logger.exception("ConnectionError")

    yield

    await app['db'].close()
    logger.info("app = close")
