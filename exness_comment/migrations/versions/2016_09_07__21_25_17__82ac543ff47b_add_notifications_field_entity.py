"""add notifications field entity

Revision ID: 82ac543ff47b
Revises: f771eb1ffa0f
Create Date: 2016-09-07 21:25:17.580588

"""

# revision identifiers, used by Alembic.
revision = '82ac543ff47b'
down_revision = 'f771eb1ffa0f'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('notifications', sa.Column('entity_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'notifications', 'entities', ['entity_id'], ['id'])
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'notifications', type_='foreignkey')
    op.drop_column('notifications', 'entity_id')
    ### end Alembic commands ###
