"""empty message

Revision ID: cf1ff8130fc8
Revises: 2b9b12d6b02e
Create Date: 2019-11-22 17:16:14.132421

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'cf1ff8130fc8'
down_revision = '2b9b12d6b02e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('events', 'event_end_time')
    op.drop_column('events', 'event_start_time')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('events', sa.Column('event_start_time', postgresql.TIMESTAMP(), autoincrement=False, nullable=False))
    op.add_column('events', sa.Column('event_end_time', postgresql.TIMESTAMP(), autoincrement=False, nullable=False))
    # ### end Alembic commands ###
