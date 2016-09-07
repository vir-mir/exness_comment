import datetime

import schema as vs
import sqlalchemy as sa
from sqlalchemy.orm import aliased

from exness_comment.middlewares.exceptions import abort
from exness_comment.models import Entity, Comment
from exness_comment.utils import tree
from exness_comment.utils.views import json_response
from exness_comment.views.commet.mixin import MixinComment

__all__ = ['Comments']


class Comments(MixinComment):
    async def get(self):
        data = dict(self.request.GET)
        schema = {
            vs.Optional('first_level', default=False): vs.Regex('[01]'),
            vs.Optional('limit', default=10): vs.Regex('[\d]+'),
            vs.Optional('page', default=1): vs.Regex('[1-9][\d]*'),
            vs.Optional('parent_id', default=0): vs.Regex('[1-9][\d]*'),
            'entity_id': vs.Regex('[1-9][\d]*'),
        }
        data = self.validate(schema, data)

        data['first_level'] = bool(int(data['first_level']))
        data['limit'] = int(data['limit'])
        data['parent_id'] = int(data['parent_id'])
        data['page'] = int(data['page'])
        data['entity_id'] = int(data['entity_id'])

        if data['first_level']:
            ret = await self.get_first_level_comments(data)
        elif data['parent_id'] > 0:
            ret = await self.get_parents_comments(data)
        else:
            ret = await self.get_entity_comments(data)

        return json_response(ret)

    async def get_first_level_comments(self, data):
        limit = data['limit']
        offset = 0 if data['page'] == 1 else data['page'] * data['limit']

        query = (sa.select(self.fields)
                 .select_from(Comment)
                 .where(sa.and_(Comment.level == 0, Comment.entity_id == data['entity_id']))
                 .limit(limit)
                 .offset(offset)
                 .order_by(Comment.date_created))

        resp = await self.request['conn'].execute(query)

        return await resp.fetchall()

    async def get_parents_comments(self, data):
        c = aliased(Comment)
        join = sa.join(c, Comment,
                       sa.and_(Comment.lkey >= c.lkey, Comment.rkey <= c.rkey, Comment.tree_id == c.tree_id))

        query = (sa.select(self.fields + [Comment.tree_id])
                 .select_from(join)
                 .where(sa.and_(c.id == data['parent_id'], Comment.entity_id == data['entity_id']))
                 .order_by(Comment.date_created, Comment.lkey))

        return await self.tree(await self.request['conn'].execute(query))

    async def get_entity_comments(self, data):
        query = (sa.select(self.fields + [Comment.tree_id])
                 .select_from(Comment)
                 .where(Comment.entity_id == data['entity_id'])
                 .order_by(Comment.date_created, Comment.lkey))

        return await self.tree(await self.request['conn'].execute(query))

    async def post(self):
        schema = {
            'user_id': vs.And(int, lambda x: x > 0),
            'entity_id': vs.And(int, lambda x: x > 0),
            vs.Optional('parent_id', default=0): vs.And(int, lambda x: x > -1),
            'text': str,
        }
        data = self.validate(schema, await self.request.json())

        query = (sa.select([Entity.id])
                 .select_from(Entity)
                 .where(Entity.id == data['entity_id']))

        conn = self.request['conn']
        if (await conn.execute(query)).rowcount == 0:
            abort(406, 'not essence id %s' % data['entity_id'])

        parent_id = data['parent_id']
        values = {
            'user_id': data['user_id'],
            'entity_id': data['entity_id'],
            'text': data['text'],
            'date_created': datetime.datetime.now(),
            'date_update': datetime.datetime.now()
        }

        comment = await tree.insert_tree(Comment, self.request['conn'], parent_id, values)
        return json_response(await comment.fetchone(), status=201)
