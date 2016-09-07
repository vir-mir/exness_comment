from exness_comment.views import *

urls = [
    ('*', '/comments', Comments),
    ('*', '/comments/users/{user_id}', CommentsUserById),
    ('*', '/comments/users/{user_id}/export.{format}', CommentsExportUserById),
    ('*', '/comments/{comment_id}', CommentById),

    ('*', '/entities', Entities),
]
