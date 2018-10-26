import re


class RemmeBlockchainInfo:

    _remme_rest = None

    def __init__(self, remme_rest):
        self._remme_rest = remme_rest

    @staticmethod
    def is_valid_batch_id(_batch_id):
        return re.match(r"^[0-9a-f]{128}$", _batch_id) is not None

    async def get_batch_by_id(self, batch_id):
        if not self.is_valid_batch_id(batch_id):
            raise Exception("Invalid batch id given.")
        params = {'id': batch_id}
        return await self._remme_rest.send_rpc_request(self._remme_rest.methods.FETCH_BATCH, params)

    def get_batches(self, query):
        raise NotImplementedError

    def get_block_by_id(self, block_id):
        raise NotImplementedError

    async def get_blocks(self, query):
        query = query if query else {"start": 0, "limit": 0}
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

