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

        query = sa.insert(Comment).values(
            user_id=data['user_id'],
            date_update=data['date_update'],
            essence_id=data['essence_id'],
            date_created=data['date_created']
        ).return_defaults(Comment.id)
        resp = await self.request['conn'].execute(query)
        entity = await resp.fetchone()

        return web.json_response(status=201)
