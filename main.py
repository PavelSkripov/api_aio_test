from aiohttp import web  # основной модуль aiohttp
from app.api.routes import setup_routes as setup_api_routes
from app.settings import config
from app.database.accessor import pg_context
from app.api.views import setup_cookie
import logging

# получение пользовательского логгера и установка уровня логирования
logger = logging.getLogger('main')
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


def setup_config(application: web.Application):
    """
        Функция запускает установку конфигурации базы данных.

        :param application: объект Application
        :type application: Application
    """
    application["config"] = config
    logger.info(f'setup_config is run, config = {config}')


def setup_routes(application: web.Application):
    """
        В этой функции производится настройка url-путей для всего приложения

        :param application: объект Application
        :type application: Application
    """
    setup_api_routes(application)
    logger.info('setup_routes is run')


def setup_app(application: web.Application):
    """
        В этой функции производится настройка всего приложения

        :param application: объект Application
        :type application: Application
    """
    setup_config(application)
    setup_routes(application)
    setup_cookie(application)


app = web.Application()  # создаем наш веб-сервер


if __name__ == "__main__":
    # эта строчка указывает, что данный файл можно запустить как скрипт
    setup_app(app)
    app.cleanup_ctx.append(pg_context)
    web.run_app(app, port=8000)  # запускаем приложение
