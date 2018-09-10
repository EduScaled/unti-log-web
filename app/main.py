import sys
import jinja2
import aiohttp_jinja2

from aiohttp import web
from views import routes
from utils import get_config, setup_static_routes

def run(argv=None):
    app = web.Application()
    app['config'] = get_config(argv)
    aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader('templates/'))
    app.add_routes(routes)  
    setup_static_routes(app)  
    web.run_app(app, host=app['config']['host'], port=app['config']['port'])

if __name__ == '__main__':
   run(sys.argv[1:])