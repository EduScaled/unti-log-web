import aiohttp_jinja2
from aiohttp import web
from service import fetch_logs

routes = web.RouteTableDef()

@routes.view('/logs/')
class LogListView(web.View):

    @aiohttp_jinja2.template('logs.html')
    async def get(self):
        data = {
            'data': await fetch_logs()
        }
        return data

    async def post(self):
        post = await self.request.post()
        params = {
            'type': post.get('type', None),
            'action': post.get('action', None),
            'date_gt': post.get('date_gt', None),
            'date_lt': post.get('date_lt', None),
        }
        if post.get('user', None):
            try:
                user_id = int(post.get('user'))
                params['user_id'] = user_id
            except ValueError:
                params['email'] = post.get('user')

        logs = await fetch_logs(params)

        return web.json_response(logs)