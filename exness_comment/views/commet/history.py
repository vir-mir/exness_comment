import schema as vs
import sqlalchemy as sa

from exness_comment.middlewares.exceptions import abort
from exness_comment.models import CommentHistory as ModelCommentHistory
from exness_comment.utils.views import json_response
from exness_comment.views.commet.mixin import MixinComment

__all__ = ['CommentHistory']


class CommentHistory(MixinComment):
    async def get(self):
        data = {'comment_id': self.request.match_info['comment_id']}
        schema = {
            'comment_id': vs.Regex('\d+'),
        }
        data = self.validate(schema, data)
        data['comment_id'] = int(data['comment_id'])

        query = sa.select([ModelCommentHistory])
        query = query.where(ModelCommentHistory.id == data['comment_id'])
        query = query.order_by(ModelCommentHistory.event_date)

        comment = await (await self.request['conn'].execute(query)).fetchall()

        if not comment:
            abort(406, 'not comment history id %s' % data['comment_id'])

        return json_response(comment)
