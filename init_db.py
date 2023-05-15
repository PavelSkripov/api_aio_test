from sqlalchemy import create_engine

from app.settings import config
from app.database.models import Users, Roles


DSN = "postgresql://{user}:{password}@{host}:{port}/{database}"


def sample_data(engine):
    """
        Функция создает в базе данных первичного пользователя с ролью admin.

        :param engine: объект Engine
        :type engine: Engine
    """
    with engine.begin() as conn:
        conn.execute(Users.insert(), [
            {'first_name': 'Pavel',
             'last_name': 'First',
             'login': 'login',
             'password': 'pass',
             'birthday': '1996-03-26',
             'registration_date': '2023-05-12 21:17:49',
             'role_id': 'admin',
             }
             ])
        conn.execute(Roles.insert(), [
            {
             'role': 'admin',
             'users_id': 1,
             }
             ])


if __name__ == '__main__':
    db_url = DSN.format(**config['postgres'])
    engine = create_engine(db_url)
    sample_data(engine)
