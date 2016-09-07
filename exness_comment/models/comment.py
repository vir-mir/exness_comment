import sqlalchemy as sa
from sqlalchemy import func

from .base import Base

__all__ = ['Entity', 'Comment']


class Entity(Base):
    """
    Сушность Блог, пост...
    """

    __tablename__ = 'entities'
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column(sa.String(255))


class Comment(Base):
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
    user_id = sa.Column(sa.Integer, index=True)
    entity_id = sa.Column(sa.Integer, sa.ForeignKey('entities.id'))
    date_created = sa.Column(sa.DateTime(timezone=True), server_default=func.now())
    date_update = sa.Column(sa.DateTime(timezone=True), server_default=func.now())
    text = sa.Column(sa.Text)

    # tree
    parent_id = sa.Column(sa.Integer, sa.ForeignKey('comments.id'), nullable=True)
    tree_id = sa.Column(sa.String(32))
    lkey = sa.Column(sa.Integer)
    rkey = sa.Column(sa.Integer)
    level = sa.Column(sa.Integer)
