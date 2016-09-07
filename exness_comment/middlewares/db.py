from functools import wraps

from aiopg.sa import create_engine

from exness_comment.configs import settings

__all__ = ['middleware_db']


async def middleware_db(app, handler):
    if 'StaticRoute' in repr(handler):
        return handler

    @wraps(handler)
    async def middleware_handler(request):
        engine = await create_engine(
            user=settings.DATA_BASE['username'],
            database=settings.DATA_BASE['db'],
            host=settings.DATA_BASE['host'],
            password=settings.DATA_BASE['password']
        )

        async with engine, engine.acquire() as conn:
            request['conn'] = conn

            return await handler(request)

    return middleware_handler
