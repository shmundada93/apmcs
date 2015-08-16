"""empty message

Revision ID: 9f6f77334e9
Revises: 17106e12f127
Create Date: 2015-08-15 15:25:05.188000

"""

# revision identifiers, used by Alembic.
revision = '9f6f77334e9'
down_revision = '17106e12f127'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('email', sa.Column('name', sa.String(length=100), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('email', 'name')
    ### end Alembic commands ###