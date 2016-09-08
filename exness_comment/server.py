import asyncio

import aiohttp_autoreload
from aiohttp import web

from exness_comment import middlewares
from exness_comment.configs import settings, urls


def create_app(loop=None):
    if loop is None:
        loop = asyncio.get_event_loop()

    if settings.DEBUG:
        aiohttp_autoreload.start()

    middleware = [getattr(middlewares, x) for x in middlewares.__all__]
    middleware.reverse()

    app = web.Application(debug=settings.DEBUG, middlewares=middleware, loop=loop)

    [app.router.add_route(*x) for x in urls.urls]

    app.router.add_static(settings.MEDIA_URL, settings.MEDIA_ROOT, name='media')

    return app


if __name__ == '__main__':
    web.run_app(create_app(), port=settings.PORT)
