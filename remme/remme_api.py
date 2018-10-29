import aiohttp_json_rpc
from enum import Enum


class RemmeAPI:

    node_address = None
    node_port = None
    ssl_mode = None
    rpc_client = None

    def __init__(self, network_config):
        self.node_address = network_config['node_address']
        self.node_port = network_config['node_port']
        self.ssl_mode = network_config['ssl_mode']
        self.rpc_client = aiohttp_json_rpc.JsonRpcClient()

    async def send_request(self, method, params=None):
        try:
            protocol = "https" if self.ssl_mode else "http"
            await self.rpc_client.connect(host=self.node_address, port=self.node_port, protocol=protocol)
        except Exception as e:
            raise Exception("Please check if your node running at {url}".format(url=self._get_url_for_request()))
        method = method.value[0]
        request_data = {'method': method}
        if params:
            request_data['params'] = params
        try:
            return await self.rpc_client.call(**request_data)
        finally:
            await self.rpc_client.disconnect()

    def _get_url_for_request(self):
        return "https://" + self.get_node_socket() if self.ssl_mode else "http://" + self.get_node_socket()

    def get_node_socket(self):
        return self.node_address + ':' + self.node_port

    def get_ssl_mode(self):
        return self.ssl_mode
