import sqlalchemy as sa
from aiohttp import web

from exness_comment.models import Entity
from exness_comment.utils.views import View

__all__ = ['Entities']


class Entities(View):
    async def get(self):
        return web.json_response([])

    async def post(self):
        schema = {
            'name': str,
        }
        data = self.validate(schema, await self.request.json())

        query = (sa.insert(Entity).values(name=data['name'])).return_defaults(Entity.id)
        resp = await self.request['conn'].execute(query)
        entity = await resp.fetchone()

        return web.json_response({'entity_id': entity.id}, status=201)
