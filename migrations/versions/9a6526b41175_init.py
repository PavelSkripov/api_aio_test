"""init

Revision ID: 9a6526b41175
Revises: 
Create Date: 2023-05-16 12:25:56.532817

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9a6526b41175'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=200), nullable=False),
    sa.Column('last_name', sa.String(length=200), nullable=False),
    sa.Column('login', sa.String(length=200), nullable=False),
    sa.Column('password', sa.String(length=200), nullable=False),
    sa.Column('birthday', sa.Date(), nullable=False),
    sa.Column('registration_date', sa.Date(), nullable=False),
    sa.Column('role', sa.String(length=200), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('roles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('role', sa.String(length=200), nullable=False),
    sa.Column('users_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['users_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('roles')
    op.drop_table('users')
    # ### end Alembic commands ###
