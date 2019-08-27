import pytest
from restaurants.app import init_app

@pytest.fixture
async def client(aiohttp_client):
    '''
    The fixture for the initialize client.
    '''
    app = init_app([])

    return await aiohttp_client(app)
