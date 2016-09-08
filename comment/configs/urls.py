from comment.views import *

urls = [
    ('*', '/comments', Comments),
    ('*', '/comments/users/{user_id}', CommentsUserById),
    ('*', '/comments/users/{user_id}/export.{format}', CommentsExportUserById),
    ('*', '/comments/history/{comment_id}', CommentHistory),
    ('*', '/comments/{comment_id}', CommentById),

    ('*', '/entities', Entities),

    ('*', '/exports', Exports),

    ('*', '/notifications', Notifications),
    ('*', '/notifications/{user_id}', NotificationById),

    ('GET', '/ws', websocket_points),
]
