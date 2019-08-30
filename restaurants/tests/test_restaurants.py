from pytest_aiohttp import aiohttp_client
from restaurants.app import init_app
from typing import List

async def fillup_data(client: aiohttp_client) -> List[str]:
    l = ['Donec vitae dolor.', 'sociis natoque penatibus et magnis',
         'Praesent fermentum', 'Sed bibendum']
    for name in l:
        resp = await client.post('/restaurants', json={"name": name})
        assert resp.status == 200
    return l

async def test_add_restaurant(client: aiohttp_client) -> None:

    resp = await client.post('/restaurants', json={"name": "Burger King"})
    assert resp.status == 200

    resp = await client.post('/restaurants', json={"name": "Burger ⋆ King"})
    assert resp.status == 200

    resp = await client.post('/restaurants', json={"name": "накоплений"})
    assert resp.status == 200


async def test_list_restaurant(client: aiohttp_client) -> None:
    inserted = await fillup_data(client)
    resp = await client.get('/restaurants')
    assert resp.status == 200
    data = await resp.json()
    assert set(inserted).issubset(data)


async def test_delete_restaurant(client: aiohttp_client) -> None:
    resp = await client.post('/restaurants', json={"name": "target"})
    assert resp.status == 200

    resp = await client.delete('/restaurants/target')
    assert resp.status == 200

    resp = await client.post('/restaurants', json={"name": "☉"})
    assert resp.status == 200

    resp = await client.delete('/restaurants/☉')
    assert resp.status == 200



async def test_delete_missing_restaurant(client: aiohttp_client) -> None:
    resp = await client.delete('/restaurants/nonexists')
    assert resp.status == 404


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


async def test_random_restaurant(client: aiohttp_client) -> None:
    # we can't really test randomness here without spending significant CPU time,
    # essentially to reduce the risks of false negatives. 
    # so we consider that "returning a restaurant without crashing" is ok.

    inserted = await fillup_data(client)
    resp = await client.get('/restaurants/random')
    assert resp.status == 200
    data = await resp.json()
    assert len(data) == 1
