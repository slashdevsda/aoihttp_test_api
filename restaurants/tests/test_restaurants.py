from pytest_aiohttp import aiohttp_client
from restaurants.app import init_app




async def test_root(client: aiohttp_client) -> None:
    '''
    Hiting the root `/` should trigger a 404 response
    '''
    resp = await client.get('/')
    assert resp.status == 404
