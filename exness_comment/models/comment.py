import sqlalchemy as sa
from sqlalchemy import func
from sqlalchemy_mptt import BaseNestedSets

from .base import Base

__all__ = ['Entity', 'Comment']


class Entity(Base):
    """
    Сушность Блог, пост...
    """

    __tablename__ = 'entities'
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column(sa.String(255))


class Comment(Base, BaseNestedSets):
    """
    Коментарии храняться в древовидной структуре по алгоритму (https://en.wikipedia.org/wiki/Nested_set_model)
    """
    __tablename__ = 'comments'
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    user_id = sa.Column(sa.Integer, index=True)
    essence_id = sa.Column(sa.Integer, sa.ForeignKey('entities.id'))
    date_created = sa.Column(sa.DateTime(timezone=True), server_default=func.now())
    date_update = sa.Column(sa.DateTime(timezone=True), server_default=func.now())
    text = sa.Column(sa.Text)
