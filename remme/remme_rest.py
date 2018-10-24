import aiohttp_json_rpc


class RemmeRest:

    node_address = None
    node_port = None
    ssl_mode = None
    node_url = None
    rpc_client = None

    def __init__(self, network_config):
        self.node_address = network_config['node_address']
        self.node_port = network_config['node_port']
        self.ssl_mode = network_config['ssl_mode']
        protocol = 'https' if self.ssl_mode else 'http'
        self.node_url = protocol + "://" + self.node_address + ":" + self.node_port
        self.rpc_client = aiohttp_json_rpc.JsonRpcClient()

    async def send_raw_transaction(self, data):
        return await self.__send_rpc_request('send_raw_transaction', {"data": data})

    async def get_node_public_key(self):
        return await self.__send_rpc_request('get_node_public_key')

    async def get_batch_status(self, _id):
        return await self.__send_rpc_request('get_batch_status', {"id": _id})

    async def get_block_number(self):
        return await self.__send_rpc_request('get_block_number')

    async def get_blocks(self, start=0, limit=0):
        return await self.__send_rpc_request('get_blocks', {"start": start, "limit": limit})

    async def set_node_key(self, private_key):
        return await self.__send_rpc_request('set_node_key', {"private_key": private_key})

    async def export_node_key(self):
        return await self.__send_rpc_request('export_node_key')

    async def get_balance(self, public_key):
        return await self.__send_rpc_request('get_balance', {"public_key": public_key})

    async def get_public_keys_list(self, public_key):
        return await self.__send_rpc_request('get_public_keys_list', public_key)

    async def get_public_key_info_by_key(self, public_key):
        return await self.__send_rpc_request('get_public_key_info', {"public_key": public_key})

    async def get_public_key_info_by_address(self, public_key_address):
        return await self.__send_rpc_request('get_public_key_info', {"public_key_address": public_key_address})

    async def get_atomic_swap_info(self, swap_id):
        return await self.__send_rpc_request('get_atomic_swap_info', {"swap_id": swap_id})

    async def get_atomic_swap_public_key(self):
        return await self.__send_rpc_request('get_atomic_swap_public_key')

    async def get_node_info(self):
        return await self.__send_rpc_request('get_node_info')

    async def __send_rpc_request(self, method, params=None):
        await self.rpc_client.connect(self.node_address, self.node_port)
        request_data = {'method': method}
        if params:
            request_data['params'] = params
        print(f"request data : {request_data}")
        return await self.rpc_client.call(**request_data)

    def get_node_socket(self):
        return self.node_address + ':' + self.node_port

    def get_ssl_mode(self):
        return self.ssl_mode
