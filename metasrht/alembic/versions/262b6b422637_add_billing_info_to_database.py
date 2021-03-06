"""Add billing info to database

Revision ID: 262b6b422637
Revises: e3e51a076756
Create Date: 2018-11-10 09:39:21.269104

"""

# revision identifiers, used by Alembic.
revision = '262b6b422637'
down_revision = 'e3e51a076756'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('user', sa.Column('stripe_customer', sa.String(256)))
    op.add_column('user', sa.Column('payment_cents',
        sa.Integer, nullable=False, server_default='0'))
    op.add_column('user', sa.Column('payment_interval',
        sa.String, server_default='monthly'))
    op.add_column('user', sa.Column('payment_due', sa.DateTime))
    op.create_table('invoice',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('created', sa.DateTime, nullable=False),
        sa.Column('updated', sa.DateTime, nullable=False),
        sa.Column('cents', sa.Integer, nullable=False),
        sa.Column('user_id', sa.Integer,
            sa.ForeignKey('user.id'), nullable=False),
        sa.Column('valid_thru', sa.DateTime, nullable=False),
        sa.Column('source', sa.String(256), nullable=False))


def downgrade():
    op.drop_column('user', 'stripe_customer')
    op.drop_column('user', 'payment_cents')
    op.drop_column('user', 'payment_interval')
    op.drop_column('user', 'payment_due')
    op.drop_table('invoice')
