"""add export comments fields url

Revision ID: e6c80e88914f
Revises: 3da8a652a9e0
Create Date: 2016-09-07 19:21:10.604167

"""

# revision identifiers, used by Alembic.
revision = 'e6c80e88914f'
down_revision = '3da8a652a9e0'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('export_comments', sa.Column('url', sa.String(length=255), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('export_comments', 'url')
    ### end Alembic commands ###
