import datetime

import schema as vs
import sqlalchemy as sa

from comment.middlewares.exceptions import abort
from comment.models import Comment, CommentHistory, Notification
from comment.utils.tree import delete_tree
from comment.utils.views import json_response
from comment.views.commet.mixin import MixinComment

__all__ = ['CommentById']


class CommentById(MixinComment):
    async def delete(self):
        data = {'comment_id': self.request.match_info['comment_id']}
        schema = {
            'comment_id': vs.Regex('\d+'),
        }
        data = self.validate(schema, data)
        data['comment_id'] = int(data['comment_id'])
        comment = await delete_tree(Comment, self.request['conn'], data['comment_id'])

        if type(comment) is not dict:
            abort(406, comment)

        query = sa.insert(CommentHistory)
        query = query.values(
            date_created=comment['date_created'],
            text=comment['text'],
            event_user=comment['user_id'],
            user_id=comment['user_id'],
            id=comment['id'],
            parent_id=comment['parent_id'] if comment['parent_id'] else 0,
            entity_id=comment['entity_id'],
            event_type=CommentHistory.TYPE.get('Delete comment')
        )

        await self.request['conn'].execute(query)

        return json_response(comment, status=202, socket_action=Notification.ACTION['Push comment'])

    async def put(self):
        data = await self.request.json()
        data.update({'comment_id': self.request.match_info['comment_id']})

        schema = {
            'comment_id': vs.Regex('\d+'),
            'text': str,
        }
        data = self.validate(schema, data)

        data['comment_id'] = int(data['comment_id'])

        query = (sa.select([Comment])
                 .select_from(Comment)
                 .where(Comment.id == data['comment_id']))

        conn = self.request['conn']
        comment = await (await conn.execute(query)).fetchone()

        if not comment:
            abort(406, 'not comment id %s' % data['comment_id'])

        query = (sa.update(Comment)
                 .values(text=data['text'], date_update=datetime.datetime.now())
                 .where(Comment.id == data['comment_id']))

        await conn.execute(query)

        comment = dict(comment)

        query = sa.insert(CommentHistory)
        query = query.values(
            date_created=comment['date_created'],
            text=comment['text'],
            id=comment['id'],
            event_user=comment['user_id'],
            user_id=comment['user_id'],
            parent_id=comment['parent_id'] if comment['parent_id'] else 0,
            entity_id=comment['entity_id'],
            event_type=CommentHistory.TYPE.get('Edit comment')
        )

        await conn.execute(query)

        return json_response(comment, status=202, socket_action=Notification.ACTION['Push comment'])
