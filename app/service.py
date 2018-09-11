import os
import sys
import socket
import aiohttp
from app.utils import get_config

argv = None
if len(sys.argv) > 1 and 'wsgi' in sys.argv[1]:
    argv = sys.argv[1].split("\"")
    if len(argv) > 1:
        argv = [None, '--config', argv[1]]
    else:
        raise Exception("Can't parse config filename")
elif os.environ.get('CONFIG', None):
    argv = [None, '--config', os.environ.get('CONFIG')]
else:
    argv = sys.argv[1:]

config = get_config(argv)

api_url = "{}://{}:{}/logs/list/".format(
    config['api']['protocol'],
    socket.gethostbyname(config['api']['host']),
    config['api']['port']
)

async def fetch_logs(params={}):
    async with aiohttp.ClientSession() as session:
        async with session.post(api_url, json=params) as response:
            if response.status == 200:
                return await response.json()
            else:
                # TODO throw html page with stack trace
                raise Exception("Remote server error while fetching log data...")