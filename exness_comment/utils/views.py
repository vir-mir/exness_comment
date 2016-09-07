import datetime
import json

import schema as vs
from aiohttp import web

from exness_comment.middlewares.exceptions import abort


class View(web.View):
    def validate(self, schema, data):
        schema = vs.Schema(schema)

        try:
            return schema.validate(data)
        except vs.SchemaError as e:
            abort(406, str(e))


class DatetimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%dT%H:%M:%SZ')
        elif isinstance(obj, datetime.date):
            return obj.strftime('%Y-%m-%d')
        return json.JSONEncoder.default(self, obj)


def dumps(data):
    return json.dumps(data, cls=DatetimeEncoder)
