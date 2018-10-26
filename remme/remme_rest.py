import aiohttp_json_rpc
from enum import Enum


class RemmeMethods(Enum):

    def __call__(self, *args, **kwargs):
        return self.value[0]

    PUBLIC_KEY = "get_public_key_info",
    TOKEN = "get_balance",
    BATCH_STATUS = "get_batch_status",
    ATOMIC_SWAP = "get_atomic_swap_info",
    ATOMIC_SWAP_PUBLIC_KEY = "get_atomic_swap_public_key",
    USER_PUBLIC_KEY = "get_public_keys_list",
    NODE_KEY = "get_node_public_key",
    NODE_PRIVATE_KEY = "export_node_key",
    TRANSACTION = "send_raw_transaction",
    NETWORK_STATUS = "get_node_info",
    BLOCK_INFO = "get_blocks",
    BLOCKS = "list_blocks",
    FETCH_BLOCK = "fetch_block",
    BATCHES = "list_batches",
    FETCH_BATCH = "fetch_batch",
    TRANSACTIONS = "list_transactions",
    FETCH_TRANSACTION = "fetch_transaction",
    STATE = "list_state",
    FETCH_STATE = "fetch_state",
    PEERS = "fetch_peers",
    RECEIPTS = "list_receipts"


class RemmeRest:

    node_address = None
    node_port = None
    ssl_mode = None
    rpc_client = None
    methods = None

    def __init__(self, network_config):
        self.node_address = network_config['node_address']
        self.node_port = network_config['node_port']
        self.ssl_mode = network_config['ssl_mode']
        self.rpc_client = aiohttp_json_rpc.JsonRpcClient()
        self.methods = RemmeMethods

    async def send_rpc_request(self, method, params=None):
        try:
            protocol = "https" if self.ssl_mode else "http"
            await self.rpc_client.connect(host=self.node_address, port=self.node_port, protocol=protocol)
        except Exception as e:
            raise Exception("Please check if your node running at {url}".format(url=self._get_url_for_request()))
        method = method() if hasattr(method, '__call__') else method
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
