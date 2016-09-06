from exness_comment.views import *

urls = [
    ('*', '/comments', Comments),

    ('*', '/entities', Entities),
]
