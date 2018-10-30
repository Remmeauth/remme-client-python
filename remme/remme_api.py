import aiohttp_json_rpc
from remme.remme_methods import RemmeMethods


class RemmeAPI:

    _node_address = None
    _ssl_mode = None
    _rpc_client = None
    _node_protocol = None
    _request_URI = None

    def __init__(self, network_config):
        self._node_address = network_config['node_address'] + ":" + network_config['node_port']
        self._ssl_mode = network_config['ssl_mode']
        self._node_protocol = "https://" if self._ssl_mode else "http://"
        self._request_URI = self._node_protocol + self._node_address
        self._rpc_client = aiohttp_json_rpc.JsonRpcClient()

    async def send_request(self, method, params=None):
        if not isinstance(method, RemmeMethods):
            raise Exception("Invalid RPC method given.")
        try:
            await self._rpc_client.connect_url(url=self._request_URI)
        except Exception as e:
            raise Exception("Please check if your node running at {url}".format(url=self._request_URI()))
        method = method.value
        request_data = {'method': method}
        if params:
            request_data['params'] = params
        try:
            return await self._rpc_client.call(**request_data)
        finally:
            await self._rpc_client.disconnect()

    @property
    def node_socket(self):
        return self._node_address

    @property
    def ssl_mode(self):
        return self._ssl_mode
