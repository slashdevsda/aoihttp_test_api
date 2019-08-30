import pytest
from restaurants.app import init_app

@pytest.fixture
async def client(aiohttp_client): # type: ignore
    '''
    HTTP client fixture
    '''
    app = init_app([])

    return await aiohttp_client(app)
