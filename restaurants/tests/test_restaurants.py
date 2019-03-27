from pytest_aiohttp import aiohttp_client
from restaurants.app import init_app



async def test_add_restaurant(client: aiohttp_client) -> None:
    
    resp = await client.post('/restaurants', json={"name": "Burger King"})
    assert resp.status == 200

    resp = await client.post('/restaurants', json={"name": "Burger ⋆ King"})
    assert resp.status == 200

    resp = await client.post('/restaurants', json={"name": "накоплений"})
    assert resp.status == 200


async def test_add_restaurant_invalids(client: aiohttp_client) -> None:
    # not JSON
    resp = await client.post('/restaurants', data=b'\x5e\xaf')
    assert resp.status == 400
    
    # malformed JSON
    resp = await client.post('/restaurants', data='{"name": " :" "Pizza King"}')
    assert resp.status == 400
    
    # invalid JSON
    resp = await client.post('/restaurants', json={"name": 123456})
    assert resp.status == 422

    # empty object
    resp = await client.post('/restaurants', json={})
    assert resp.status == 422
    
    # outrageously invalid JSON
    resp = await client.post('/restaurants', json={"☃": "name"})
    assert resp.status == 422

    # unwanted properties
    resp = await client.post('/restaurants', json={"name": "Pizza", "base": "tomatoes"})
    assert resp.status == 422


async def test_root(client: aiohttp_client) -> None:
    '''
    Hiting the root `/` should trigger a 404 response
    '''
    resp = await client.get('/')
    assert resp.status == 404
