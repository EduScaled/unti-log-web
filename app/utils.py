import pathlib
import trafaret as T

from trafaret_config import commandline

PROJECT_ROOT = pathlib.Path(__file__).parent

class Options():

    def __init__(self, config):
        self.config = config
        self.print_config_vars = False
        self.print_config = False
        self.check_config = False

TRAFARET = T.Dict({
    T.Key('host'): T.IP,
    T.Key('port'): T.Int(),
    T.Key('api'):
        T.Dict({
            'protocol': T.String(),
            'host': T.IP,
            'port': T.Int(),
        })
})

def get_config():
    options = Options('../config/dev.yaml')
    config = commandline.config_from_options(options, TRAFARET)

    return config

def setup_static_routes(app):
    app.router.add_static('/static/', path=PROJECT_ROOT / 'static', name='static')