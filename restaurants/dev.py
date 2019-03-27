from aiohttp import web
from restaurants.app import init_app

__doc__ = '''This file is an helper, allows to run the API using the command line'''

if __name__ == '__main__':
    app = init_app()
    print("Running aiohttp server")
    web.run_app(app)
