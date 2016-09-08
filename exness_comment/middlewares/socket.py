import json
from functools import wraps

import aiohttp

__all__ = ['middleware_socket']


async def middleware_socket(app, handler):
    @wraps(handler)
    async def middleware_handler(request):
        response = await handler(request)
        if 'socket_action' not in vars(response):
            return response

        data = {
            'action': response.socket_action,
            'event': request.method
        }

        if response.socket_action == 'comment':
            data['comment'] = json.loads(response.body.decode())
        else:
            return response

        session = aiohttp.ClientSession(loop=app.loop)

        try:
            async with session.ws_connect('ws://%s/ws' % request.host) as ws:
                ws.send_str('open-0')
                ws.send_str(json.dumps(data))
        except aiohttp.ClientOSError:
            pass
        finally:
            session.close()

        return response

    return middleware_handler
