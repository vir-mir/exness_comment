import datetime
import os

import schema as vs
import sqlalchemy as sa
from aiohttp import web

from exness_comment.configs import settings
from exness_comment.models import Comment
from exness_comment.models.export import ExportComment
from exness_comment.utils.export import factory_export
from exness_comment.utils.views import json_response
from exness_comment.views.commet.mixin import MixinComment

__all__ = ['CommentsUserById', 'CommentsExportUserById']


class CommentsUserById(MixinComment):
    async def get(self):
        data = {'user_id': self.request.match_info['user_id']}
        schema = {
            'user_id': vs.Regex('\d+'),
        }
        data = self.validate(schema, data)
        data['user_id'] = int(data['user_id'])

        query = (sa.select(self.fields)
                 .select_from(Comment)
                 .where(Comment.user_id == data['user_id'])
                 .order_by(Comment.date_created))

        comments = await (await self.request['conn'].execute(query)).fetchall()

        return json_response(comments)


class CommentsExportUserById(MixinComment):
    async def get(self):
        data = {
            'user_id': self.request.match_info['user_id'],
            'format': self.request.match_info['format'],
        }
        data.update(dict(self.request.GET))

        schema = {
            'user_id': vs.Regex('\d+'),
            vs.Optional('date_start', default=None): vs.Regex('\d{4,4}-\d{2,2}-\d{2,2}'),
            vs.Optional('date_end', default=None): vs.Regex('\d{4,4}-\d{2,2}-\d{2,2}'),
            'format': vs.Or('json', 'xml'),
        }

        data = self.validate(schema, data)
        data['user_id'] = int(data['user_id'])

        query_export = sa.insert(ExportComment)

        where = [Comment.user_id == data['user_id']]

        if data['date_start'] and data['date_end']:
            data['date_start'] = datetime.datetime.strptime(data['date_start'], '%Y-%m-%d')
            data['date_end'] = datetime.datetime.strptime(data['date_end'], '%Y-%m-%d')
            where.append(sa.between(Comment.date_created, data['date_start'], data['date_end']))

        query = (sa.select(self.fields)
                 .select_from(Comment)
                 .where(sa.and_(*where))
                 .order_by(Comment.date_created))

        comments = await self.request['conn'].execute(query)

        export = factory_export(data['format'])
        date = datetime.datetime.now()

        name = 'export-user-{}-{}.{}'.format(data['user_id'], date.strftime('%Y_%m_%d_%H_%M_%S'), data['format'])
        data_export = await export(comments)

        filename = os.path.join(settings.MEDIA_ROOT, 'exports', name)
        url = os.path.join(settings.MEDIA_URL, 'exports', name)

        data.update({'url': url})
        query_export = query_export.values(**data)

        with open(filename, 'w+b') as f:
            f.write(data_export)
            await self.request['conn'].execute(query_export)

        return web.HTTPFound(url)
