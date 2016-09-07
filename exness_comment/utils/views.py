import datetime
import json

import schema as vs
from aiohttp import web
from aiopg.sa.result import RowProxy

from exness_comment.middlewares.exceptions import abort


class View(web.View):
    def validate(self, schema, data):
        schema = vs.Schema(schema)

        try:
            return schema.validate(data)
        except vs.SchemaError as e:
            abort(406, str(e))


class EncoderJson(json.JSONEncoder):
    def default(self, obj):

        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%dT%H:%M:%SZ')
        elif isinstance(obj, datetime.date):
            return obj.strftime('%Y-%m-%d')
        elif isinstance(obj, RowProxy):
            return dict(obj)

        return json.JSONEncoder.default(self, obj)


def json_response(data=None, *, body=None, status=200, reason=None, headers=None,
                  content_type='application/json', socket_action=False):
    text = json.dumps(data, cls=EncoderJson)

    response = web.Response(text=text, body=body, status=status, reason=reason, headers=headers,
                            content_type=content_type)

    if socket_action:
        response.socket_action = socket_action

    return response
