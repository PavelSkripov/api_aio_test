import pathlib
import yaml

BASE_DIR = pathlib.Path(__file__).parent.parent
config_path = BASE_DIR / 'config' / 'config.yaml'


def get_config(path: pathlib.PosixPath):
    """
        Функция получает конфигурацию из файла.

        :param path: объект PosixPath
        :type path: PosixPath
    """
    with open(path) as f:
        config = yaml.safe_load(f)
    return config


config = get_config(config_path)
