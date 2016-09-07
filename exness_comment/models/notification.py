import sqlalchemy as sa
from sqlalchemy import func
from sqlalchemy.dialects import postgresql

from exness_comment.models.base import Base

__all__ = ['Notification']


class Notification(Base):
    __tablename__ = 'notifications'

    ACTION = {
        'Push comment': 'comment',
    }

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    date_create = sa.Column(sa.DateTime(timezone=True), server_default=func.now())
    user_id = sa.Column(sa.Integer)
    entity_id = sa.Column(sa.Integer, sa.ForeignKey('entities.id'))
    action = sa.Column(postgresql.ENUM(*list(ACTION.values()), name='action', create_type=False))
