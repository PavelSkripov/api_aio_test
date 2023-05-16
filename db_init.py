import asyncio
import asyncpg
import datetime
from app.settings import config


DSN = "postgresql://{user}:{password}@{host}:{port}/{database}"


async def sample_data():
    """
        Функция создает в базе данных первичного пользователя с ролью admin.
    """
    db_url = DSN.format(**config['postgres'])
    conn = await asyncpg.connect(db_url)
    await conn.fetchrow("INSERT into Users(first_name, last_name, login,\
                        password, birthday, registration_date, role)\
                        values ($1, $2, $3, $4, $5, $6, $7) returning id",
                        'Pavel',
                        'First',
                        'login',
                        'pass',
                        datetime.datetime.now(),
                        datetime.datetime.now(),
                        'admin',
                        )

    await conn.fetchrow("INSERT into Roles(role, users_id) values ($1, $2)\
                        returning *",
                        'admin',
                        1,
                        )

    # Select a row from the table.
    row = await conn.fetchrow(
        'SELECT * FROM Users WHERE first_name = $1', 'Pavel')
    print(f'row {row}')
    await conn.close()

asyncio.get_event_loop().run_until_complete(sample_data())
