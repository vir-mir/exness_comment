"""delete field history comments

Revision ID: 8f937b231579
Revises: e6c80e88914f
Create Date: 2016-09-07 19:42:13.048422

"""

# revision identifiers, used by Alembic.
revision = '8f937b231579'
down_revision = 'e6c80e88914f'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('comments_history', 'date_update')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('comments_history', sa.Column('date_update', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('now()'), autoincrement=False, nullable=True))
    ### end Alembic commands ###
