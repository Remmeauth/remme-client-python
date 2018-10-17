import aiohttp

OK = 200

GET = 'get'
POST = 'post'
PUT = 'put'
DELETE = 'delete'


class RemmeRest:

    node_address = None
    node_port = None
    ssl_mode = None
    node_url = None

    def __init__(self, network_config):
        self.node_address = network_config['node_address']
        self.node_port = network_config['node_port']
        self.ssl_mode = network_config['ssl_mode']
        protocol = 'https' if self.ssl_mode else 'http'
        self.node_url = protocol + "://" + self.node_address + ":" + self.node_port

    async def _send_request(self, request_type, route, data=None):
        session = aiohttp.ClientSession()
        url = self.node_url + route
        request_method = getattr(session, request_type)
        kwargs = {}
        if request_type == GET and data:
            kwargs['params'] = data
        if request_type != GET:
            kwargs['json'] = data
        async with request_method(url, **kwargs) as resp:
            try:
                if resp.status == OK:
                    return {'status': "OK", 'data': await resp.json()}
                return {'status': "ERROR"}
            finally:
                await session.close()

    async def get(self, route):
        return await self._send_request(GET, route)

    async def post(self, route, data):
        return await self._send_request(POST, route, data)

    async def put(self, route, data):
        return await self._send_request(PUT, route, data)

    async def delete(self, route, data):
        return await self._send_request(DELETE, route, data)

    def get_node_socket(self):
        return self.node_address + ':' + self.node_port

    def get_ssl_mode(self):
        return self.ssl_mode
