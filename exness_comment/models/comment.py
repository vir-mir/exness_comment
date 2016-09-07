import sqlalchemy as sa
from sqlalchemy import func
from sqlalchemy.dialects import postgresql
from sqlalchemy.ext.declarative import declared_attr

from .base import Base

__all__ = ['Entity', 'Comment', 'CommentHistory']


class Entity(Base):
    """
    Сушность Блог, пост...
    """

    __tablename__ = 'entities'
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column(sa.String(255))


class CommentMixin:
    __tablename__ = ''
    user_id = sa.Column(sa.Integer, index=True)
    date_created = sa.Column(sa.DateTime(timezone=True), server_default=func.now())
    text = sa.Column(sa.Text)

    @declared_attr
    def parent_id(cls):
        if cls.__tablename__ == 'comments':
            return sa.Column(sa.Integer, sa.ForeignKey('comments.id'), nullable=True)
        return sa.Column(sa.Integer, nullable=True)

    @declared_attr
    def entity_id(cls):
        return sa.Column(sa.Integer, sa.ForeignKey('entities.id'))


class Comment(CommentMixin, Base):
    """
    Коментарии храняться в древовидной структуре по алгоритму (https://en.wikipedia.org/wiki/Nested_set_model)

    level           Nested sets example

    ----------------------------------------------------------
    1               |    1(1)22                               |
            ________|______|_____________________             |
           |        |      |                     |            |
           |         ------+---------            |            |
    2    2(2)5           6(4)11      | --     12(7)21         |
           |               ^             |   /      \         |
    3    3(3)4       7(5)8   9(6)10      ---/----    \        |
                                        13(8)16 |  17(10)20   |
                                           |    |     |       |
    4                                   14(9)15 | 18(11)19    |
                                                |             |
                                                 -------------
    """

    __tablename__ = 'comments'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    date_update = sa.Column(sa.DateTime(timezone=True), server_default=func.now())
    tree_id = sa.Column(sa.String(32))
    lkey = sa.Column(sa.Integer)
    rkey = sa.Column(sa.Integer)
    level = sa.Column(sa.Integer)


class CommentHistory(CommentMixin, Base):
    TYPE = {
        'add': "Add comment",
        'update': "Edit comment",
        'delete': "Delete comment",
    }
    __tablename__ = 'comments_history'

    event_id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    id = sa.Column(sa.Integer, nullable=True)
    event_user = sa.Column(sa.Integer, index=True)
    event_date = sa.Column(sa.DateTime(timezone=True), server_default=func.now())
    event_type = sa.Column(postgresql.ENUM(*list(TYPE.keys()), name='event_type', create_type=False))
