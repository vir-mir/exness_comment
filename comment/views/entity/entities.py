import sqlalchemy as sa

from comment.models import Entity
from comment.utils.views import View, json_response

__all__ = ['Entities']


class Entities(View):
    async def get(self):
        entities = await (await self.request['conn'].execute(sa.select([Entity]))).fetchall()
        return json_response(entities)

    async def post(self):
        schema = {
            'name': str,
        }
        data = self.validate(schema, await self.request.json())

        query = (sa.insert(Entity).values(name=data['name'])).return_defaults(Entity.id)
        resp = await self.request['conn'].execute(query)
        entity = await resp.fetchone()

        return json_response({'entity_id': entity.id}, status=201)
