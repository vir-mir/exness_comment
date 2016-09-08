import sqlalchemy as sa
from sqlalchemy import func

from comment.models.base import Base

__all__ = ['ExportComment']


class ExportComment(Base):
    __tablename__ = 'export_comments'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    date_create = sa.Column(sa.DateTime(timezone=True), server_default=func.now())
    date_start = sa.Column(sa.DateTime(timezone=True), nullable=True)
    date_end = sa.Column(sa.DateTime(timezone=True), nullable=True)
    format = sa.Column(sa.String(50))
    user_id = sa.Column(sa.Integer)
    url = sa.Column(sa.String(255))
