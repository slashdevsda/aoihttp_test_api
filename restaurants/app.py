from textwrap import wrap
from aiohttp import web
import aiosqlite
from typing import Optional, List, AsyncGenerator

async def database_connect(app: web.Application) -> AsyncGenerator[None, None]:
    '''
    This coroutine is responsible for database initialization.

    As we use an in-memory sqlite (for the sake of simplicity),
    initialisation and data-insertion is done right here
    '''
    db = await aiosqlite.connect(":memory:")
    app['db'] = db
    await db.execute(wrap('''
      CREATE DATABASE test(name VARCHAR);
    '''))
    yield 
    await db.close()
    
    

async def test_handler(request: web.Request) -> web.Response:
    return web.Response(status=200)
    
def init_app(config: Optional[List[str]] = None) -> web.Application:
    app = web.Application()


    
    # init context here
    # - configuration
    # - routes
    # - database connexions
    # - enventual template engines
    app.router.add_route('GET', '/test', test_handler)
    app.cleanup_ctx.extend([])
    return app
