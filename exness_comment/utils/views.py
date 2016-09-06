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
