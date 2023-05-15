from sqlalchemy import (
    MetaData, Table, Column, ForeignKey,
    Integer, String, Date
)


meta = MetaData()

Users = Table(
    'users', meta,

    Column('id', Integer, primary_key=True),
    Column('first_name', String(200), nullable=False),
    Column('last_name', String(200), nullable=False),
    Column('login', String(200), nullable=False),
    Column('password', String(200), nullable=False),
    Column('birthday', Date, nullable=False),
    Column('registration_date', Date, nullable=False),
    Column('role', String(200), nullable=False),
)

Roles = Table(
    'roles', meta,

    Column('id', Integer, primary_key=True),
    Column('role', String(200), nullable=False),
    Column('users_id',
           Integer,
           ForeignKey('users.id', ondelete='CASCADE'))
)
