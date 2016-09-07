import aiohttp_autoreload
from aiohttp import web

from exness_comment import middlewares
from exness_comment.configs import settings, urls

if settings.DEBUG:
    aiohttp_autoreload.start()

middleware = [getattr(middlewares, x) for x in middlewares.__all__]
middleware.reverse()

app = web.Application(debug=settings.DEBUG, middlewares=middleware)

[app.router.add_route(*x) for x in urls.urls]

app.router.add_static(settings.MEDIA_URL, settings.MEDIA_ROOT, name='media')

web.run_app(app, port=settings.PORT)
