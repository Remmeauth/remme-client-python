
class RemmeBlockchainInfo:

    _remme_rest = None

    def __init__(self, remme_rest):
        self._remme_rest = remme_rest

    def get_batch_by_id(self, batch_id):
        raise NotImplementedError

    def get_batches(self, query):
        raise NotImplementedError

    def get_block_by_id(self, block_id):
        raise NotImplementedError

    async def get_blocks(self, query):
        query = query if query else {"start": 0, "limit": 0}
        print(self._remme_rest.methods.BLOCK_INFO)
        return await self._remme_rest.send_rpc_request(self._remme_rest.methods.BLOCK_INFO, params=query)

    def get_peers(self):
        raise NotImplementedError

    def get_receipts(self):
        raise NotImplementedError

    def get_state(self):
        raise NotImplementedError

    def get_state_by_address(self, address):
        raise NotImplementedError

    def get_transaction_by_id(self, tx_id):
        raise NotImplementedError

    def get_transactions(self, query):
        raise NotImplementedError

    async def get_network_status(self):
        return await self._remme_rest.send_rpc_request(self._remme_rest.methods.NETWORK_STATUS)

    def get_block_info(self, query):
        raise NotImplementedError

