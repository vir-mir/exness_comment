import schema as vs
import sqlalchemy as sa

from exness_comment.middlewares.exceptions import abort
from exness_comment.models import Notification, Entity
from exness_comment.utils.views import View, json_response

__all__ = ['Notifications', 'NotificationById']


class Notifications(View):
    async def post(self):
        data = await self.request.json()
        schema = {
            'entity_id': vs.And(int, lambda x: x > 0),
            'user_id': vs.And(int, lambda x: x > 0),
        }

        query = (sa.select([Entity.id])
                 .select_from(Entity)
                 .where(Entity.id == data['entity_id']))

        conn = self.request['conn']
        if (await conn.execute(query)).rowcount == 0:
            abort(406, 'not essence id %s' % data['entity_id'])

        data = self.validate(schema, data)
        query = sa.insert(Notification).values(
            action=Notification.ACTION['Push comment'],
            entity_id=data['entity_id'],
            user_id=data['user_id'],
        )

        await self.request['conn'].execute(query)

        return json_response(status=202)


class NotificationById(View):
    async def delete(self):
        data = await self.request.json()
        data['user_id'] = self.request.match_info['user_id']

        schema = {
            'entity_id': vs.And(int, lambda x: x > 0),
            'user_id': vs.Regex('\d+'),
        }
        data = self.validate(schema, data)
        data['user_id'] = int(data['user_id'])

        query = sa.delete(Notification).where(sa.and_(
            Notification.user_id == data['user_id'],
            Notification.entity_id == data['entity_id'],
            Notification.action == Notification.ACTION['Push comment']
        ))

        await self.request['conn'].execute(query)

        return json_response(status=201)
