from exness_comment.views import *

urls = [
    ('*', '/comments', Comments),
    ('*', '/comments/{comment_id}', CommentById),

    ('*', '/entities', Entities),
]
