import aiohttp
from utils import get_config

config = get_config()

api_url = "{}://{}:{}/logs/list/".format(
    config['api']['protocol'],
    config['api']['host'],
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