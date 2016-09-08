import pytest


@pytest.fixture
def schema_comment():
    return {
        'type': 'object',
        'properties': {
            'date_created': {'type': 'string'},
            'date_update': {'type': 'string'},
            'text': {'type': 'string'},
            'level': {'type': 'integer'},
            'id': {'type': 'integer'},
            'user_id': {'type': 'integer'},
        },
        'required': ['date_created', 'date_update', 'text', 'level', 'id', 'user_id']
    }


@pytest.fixture
def schema_comments(schema_comment):
    def schema(*, min_item=None, max_item=None, parent=False):
        s = {
            'type': 'array',
            'items': schema_comment
        }

        if min_item:
            s['minItems'] = min_item

        if max_item:
            s['maxItems'] = max_item

        if parent:
            schema_comment['children'] = {
                'type': 'array',
                'items': dict(schema_comment)
            }

        return s

    return schema


@pytest.fixture
def schema_comments_history():
    return {
        'type': 'array',
        'items': {
            'type': 'object',
            'properties': {
                "entity_id": {'type': 'integer'},
                "event_id": {'type': 'integer'},
                "text": {'type': 'string'},
                "parent_id": {'type': 'integer'},
                "date_created": {'type': 'string'},
                "event_date": {'type': 'string'},
                "id": {'type': 'integer'},
                "event_user": {'type': 'integer'},
                "user_id": {'type': 'integer'},
                "event_type": {'type': 'string'}
            }
        }
    }
