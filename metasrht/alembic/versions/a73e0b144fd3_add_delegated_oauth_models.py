"""Add delegated oauth models

Revision ID: a73e0b144fd3
Revises: e5f8d19beac2
Create Date: 2017-04-09 22:36:59.095173

"""

# revision identifiers, used by Alembic.
revision = 'a73e0b144fd3'
down_revision = 'e5f8d19beac2'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('oauthscope')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('oauthscope',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('created', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
    sa.Column('updated', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
    sa.Column('client_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('name', sa.VARCHAR(length=256), autoincrement=False, nullable=False),
    sa.Column('description', sa.VARCHAR(length=512), autoincrement=False, nullable=False),
    sa.Column('write', sa.BOOLEAN(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['client_id'], ['oauthclient.id'], name='oauthscope_client_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='oauthscope_pkey')
    )
    # ### end Alembic commands ###
