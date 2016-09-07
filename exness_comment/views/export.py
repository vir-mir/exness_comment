import sqlalchemy as sa

from exness_comment.models import ExportComment
from exness_comment.utils.views import View, json_response

__all__ = ['Exports']


class Exports(View):
    async def get(self):
        query = sa.select([ExportComment]).order_by(ExportComment.date_create)
        resp = await self.request['conn'].execute(query)
        reports = await resp.fetchall()

        return json_response(reports)
