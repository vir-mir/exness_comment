import datetime

import schema as vs
import sqlalchemy as sa
from aiohttp import web

from exness_comment.middlewares.exceptions import abort
from exness_comment.models import Entity, Comment
from exness_comment.utils.views import View

__all__ = ['Comments']


class Comments(View):
    async def get(self):
        return web.json_response([])

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

        # query = sa.insert(Comment).values(
        #     user_id=data['user_id'],
        #     date_update=data['date_update'],
        #     essence_id=data['essence_id'],
        #     date_created=data['date_created']
        # ).return_defaults(Comment.id)
        # resp = await self.request['conn'].execute(query)
        # entity = await resp.fetchone()

        lft = 0
        rgt = 1
        level = 0

        query = (sa.select([Comment.right, Comment.left, Comment.level])
                 .select_from(Comment)
                 .where(Comment.id == data['parent_id']))

        parent_comment = await (await conn.execute(query)).fetchone()

        query = (sa.update(Comment)
                 .values(rgt=Comment.right + 2,
                         lft=sa.case([(Comment.left > parent_comment.rgt, Comment.left + 2)], else_=Comment.left))
                 .where(Comment.right >= parent_comment.rgt))
        print(query)
        resp = await self.request['conn'].execute(query)

        query = sa.insert(Comment).values(
            user_id=data['user_id'],
            essence_id=data['entity_id'],
            text=data['text'],
            level=1,
            lft=lft + parent_comment.rgt,
            rgt=parent_comment.rgt + 1,
            parent_id=None if data['parent_id'] == 0 else data['parent_id'],
            tree_id=1,
            date_created=datetime.datetime.now(),
            date_update=datetime.datetime.now()
        ).return_defaults(Comment)

        print(query)
        resp = await self.request['conn'].execute(query)

        # print(await resp.fetchone())

        return web.json_response(status=201)
