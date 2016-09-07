import schema as vs
import sqlalchemy as sa
from aiohttp import web

from exness_comment.middlewares.exceptions import abort
from exness_comment.models import Comment
from exness_comment.views.commet.mixin import MixinComment

__all__ = ['CommentById']


class CommentById(MixinComment):
    async def put(self):
        data = await self.request.json()
        data.update({'comment_id': self.request.match_info['comment_id']})

        schema = {
            'comment_id': vs.Regex('\d+'),
            'text': str,
        }
        data = self.validate(schema, data)

        data['comment_id'] = int(data['comment_id'])

        query = (sa.select([Comment.id])
                 .select_from(Comment)
                 .where(Comment.id == data['comment_id']))

        conn = self.request['conn']
        if (await conn.execute(query)).rowcount == 0:
            abort(406, 'not comment id %s' % data['comment_id'])

        query = (sa.update(Comment)
                 .values(text=data['text'])
                 .where(Comment.id == data['comment_id']))

        await conn.execute(query)

        return web.json_response(status=202)
