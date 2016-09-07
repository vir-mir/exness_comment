from exness_comment.models import Comment
from exness_comment.utils.views import View


class MixinComment(View):
    @property
    def fields(self):
        return [
            Comment.id,
            Comment.date_created,
            Comment.date_update,
            Comment.parent_id,
            Comment.level,
            Comment.user_id,
            Comment.text,
        ]

    async def tree(self, data):
        comments_tree = []
        parents = {}

        async for comment in data:
            comment = dict(comment)
            comment['children'] = []
            key_parent = '%r%s' % (comment['parent_id'], comment['tree_id'])
            key = '%r%s' % (comment['id'], comment['tree_id'])
            del comment['tree_id']
            if key_parent in parents:
                parents[key_parent]['children'].append(comment)
            else:
                comments_tree.append(comment)

            parents.setdefault(key, comment)

        del parents

        return comments_tree
