import os
import sys
import jinja2
import aiohttp_jinja2

from aiohttp import web
from app.views import routes
from app.utils import get_config, setup_static_routes

def init_app(argv=None):
    app = web.Application(middlewares=[
       web.normalize_path_middleware(append_slash=True, merge_slashes=True),
    ])

    app['config'] = get_config(argv)

    aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader('app/templates/'))

    app.add_routes(routes)    
    
    setup_static_routes(app)  

    return app

def container():
    argv = None
    if os.environ.get('CONFIG', None):
        argv = [None, '--config', os.environ.get('CONFIG')]
    return init_app(argv)        

def wsgi(config=None):
    if config:
        argv = [None, '--config', config]
        return init_app(argv)

def run(argv=None):
    app = init_app(argv)
    web.run_app(app, host=app['config']['host'], port=app['config']['port'])