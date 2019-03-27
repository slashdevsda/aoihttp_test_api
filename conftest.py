import pytest
from restaurants.app import init_app

@pytest.fixture
async def client(aiohttp_client): # type: ignore
    '''
    The fixture for the initialize client.
    '''
    app = init_app([])

    return await aiohttp_client(app)


#Callable[[Coroutine[Request, None, Response]], Coroutine[Any, Any, Response]]", expected "Coroutine[Request, None, Response
