import json

import aiohttp
import sqlalchemy as sa
from aiohttp import web

from comment.models import Notification

wss = {}

__all__ = ['websocket_points']


class SocketException(Exception):
    pass


async def websocket_points(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    async for msg in ws:
        if msg.tp == aiohttp.MsgType.text:
            if msg.data == 'close':
                await ws.close()
            elif 'open' == msg.data[:4]:
                try:
                    ws.user_id = int(msg.data[5:])
                    wss[ws.user_id] = ws
                    ws.send_str('good open')
                except ValueError:
                    ws.send_str('error format')
                    break
            else:
                try:
                    data = json.loads(msg.data)
                    try:
                        method = factory_method(data['action'])
                    except KeyError:
                        raise SocketException

                    await method(request, data)
                except (json.JSONDecodeError, SocketException):
                    ws.send_str('error format')
                    break

        elif msg.tp == aiohttp.MsgType.error:
            print('ws connection closed with exception %s' % ws.exception())

    if 'user_id' in vars(ws) and ws.user_id in wss:
        del wss[ws.user_id]

    return ws


async def comment_point(request, data):
    conn = request['conn']

    query = sa.select([Notification.user_id])
    query = query.where(sa.and_(
        Notification.user_id.in_(wss.keys()),
        Notification.entity_id == data['comment']['entity_id'],
        Notification.action == Notification.ACTION.get('Push comment')
    ))

    notifications_wws = filter(lambda x: x.user_id in wss, await conn.execute(query))
    data = json.dumps(data)

    for notification_ws in notifications_wws:
        wss[notification_ws.user_id].send_str(data)


def factory_method(action):
    method = {
        'comment': comment_point
    }

    return method[action]
