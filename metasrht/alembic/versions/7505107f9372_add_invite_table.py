"""Add invite table

Revision ID: 7505107f9372
Revises: e3dc9b1bcf42
Create Date: 2017-04-06 18:46:25.124808

"""

# revision identifiers, used by Alembic.
revision = '7505107f9372'
down_revision = 'e3dc9b1bcf42'

from alembic import op
import sqlalchemy as sa


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('invite', sa.Column('invite_hash', sa.String(length=128), nullable=True))
    op.drop_column('invite', 'confirmation_hash')
    op.drop_column('invite', 'email')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('invite', sa.Column('email', sa.VARCHAR(length=256), autoincrement=False, nullable=False))
    op.add_column('invite', sa.Column('confirmation_hash', sa.VARCHAR(length=128), autoincrement=False, nullable=True))
    op.drop_column('invite', 'invite_hash')
    # ### end Alembic commands ###
