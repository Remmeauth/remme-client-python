import aiohttp_json_rpc


class RemmeRest:

    node_address = None
    node_port = None
    ssl_mode = None
    rpc_client = None

    def __init__(self, network_config):
        self.node_address = network_config['node_address']
        self.node_port = network_config['node_port']
        self.ssl_mode = network_config['ssl_mode']
        self.rpc_client = aiohttp_json_rpc.JsonRpcClient()

    async def send_rpc_request(self, method, params=None):
        await self.rpc_client.connect(self.node_address, self.node_port)
        request_data = {'method': method}
        if params:
            request_data['params'] = params
        # print(f"request data : {request_data}")
        return await self.rpc_client.call(**request_data)

    def get_node_socket(self):
        return self.node_address + ':' + self.node_port

    def get_ssl_mode(self):
        return self.ssl_mode
