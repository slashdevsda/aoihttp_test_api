import os
import json
import functools
from aiohttp import web
import sqlite3
import aiosqlite
from jsonschema import Draft4Validator
from jsonschema.exceptions import ValidationError

from typing import Optional, List, AsyncGenerator, Coroutine, Dict, Any, Callable

async def database_connect(app: web.Application) -> AsyncGenerator[None, None]:
    '''
    This coroutine is responsible for database initialization.

    As we use an in-memory sqlite (for the sake of simplicity),
    initialisation and data-insertion is done right here
    '''
    db = await aiosqlite.connect(os.environ.get("SQLITE_DB", ":memory:"))
    app['db'] = db
    try:
        await db.execute('CREATE TABLE restaurants(name VARCHAR);')
    except sqlite3.OperationalError:
        # already exists
        pass

    yield 
    await db.close()
    

def parse_and_validate_json_body(schema: Dict[str, Any]) -> Callable[..., Any]:
    '''
    adds an additional argument (data) to handler, containing 
    the result of a JSON deserialization from the request's body content.

    It takes a schema (JSON schema flavored) as argument and validates the incoming
    payload against it.

    If deserialization or validation fails, returns an http error to the client.
    '''
    validator = Draft4Validator(schema)
    
    def wrapper(aiohttp_handler: Callable[..., Any]) -> Callable[..., Any]:
        @functools.wraps(aiohttp_handler)
        async def p_handler(request: web.Request) -> web.Response:
            try:
                data = await request.json()
                validator.validate(data)
            except (UnicodeDecodeError, json.decoder.JSONDecodeError):
                return web.Response(status=400)
            except ValidationError:
                return web.Response(status=422)

            # execute original handler
            # (we don't to stay in the above try...catch to avoid
            # unwanted exception handling.)
            return await aiohttp_handler(request, data)
        return p_handler
    return wrapper

@parse_and_validate_json_body({
    'type': 'object',
    'properties': {
        'name': {
            'type': 'string'
            }
        },
    'additionalProperties': False,
    'required': ['name']
})
async def add_restaurant(request: web.Request, data: Dict[str, Any]={}) -> web.Response:
    await request.app['db'].execute(
        '''INSERT INTO restaurants(name)
           VALUES (?);''', (data['name'],))
    await request.app['db'].commit()
    return web.Response(status=201)


async def list_restaurant(request: web.Request) -> web.Response:
    '''
    list entries. This one is pretty straightforward an lacks of pagination
    '''
    c = await request.app['db'].execute('SELECT name FROM restaurants')
    return web.json_response(data=[i[0] for i in await c.fetchmany(200)])


async def delete_restaurant(request: web.Request) -> web.Response:
    '''
    list entries. This one is pretty straightforward an lacks of pagination
    '''
    restaurant_name = request.match_info['name']

    async with request.app['db'].cursor() as c:
        await c.execute('DELETE FROM restaurants WHERE name = ?', (restaurant_name,))
        if c.rowcount != 0:
            return web.Response(status=200)
    return web.Response(status=404)


async def random_restaurant(request: web.Request) -> web.Response:
    '''
    list entries. This one is pretty straightforward an lacks of pagination
    '''
    query = 'SELECT name FROM restaurants ORDER BY RANDOM() LIMIT 1'
    c = await request.app['db'].execute(query)
    return web.json_response(data=await c.fetchone())


def init_app(config: Optional[List[str]] = None) -> web.Application:
    app = web.Application()    
    app.router.add_route('POST', '/restaurants', add_restaurant)
    app.router.add_route('GET',  '/restaurants', list_restaurant)
    app.router.add_route('GET',  '/restaurants/random', random_restaurant)
    app.router.add_route('DELETE',  '/restaurants/{name}', delete_restaurant)
    app.cleanup_ctx.extend([database_connect])
    return app
