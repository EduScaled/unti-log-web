import argparse
import pathlib
import trafaret as T

from trafaret_config import commandline

BASE_DIR = pathlib.Path(__file__).parent.parent
PROJECT_ROOT = pathlib.Path(__file__).parent
DEFAULT_CONFIG_PATH = BASE_DIR / 'config' / 'dev.yaml'

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

def get_config(argv=None):

    ap = argparse.ArgumentParser()
    commandline.standard_argparse_options(
        ap,
        default_config=DEFAULT_CONFIG_PATH
    )

    options, unknown = ap.parse_known_args(argv)
    config = commandline.config_from_options(options, TRAFARET)

    return config

def setup_static_routes(app):
    app.router.add_static('/static/', path=PROJECT_ROOT / 'static', name='static')