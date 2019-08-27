from aiohttp import web
from typing import Optional, List

def init_app(config: Optional[List[str]] = None) -> web.Application:
    app = web.Application()

    # init context here
    # - configuration
    # - routes
    # - database connexions
    # - enventual template engines
    app.cleanup_ctx.extend([])
    return app
