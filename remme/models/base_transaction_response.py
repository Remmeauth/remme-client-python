from remme.remme_websocket import RemmeWebSocket


class BaseTransactionResponse(RemmeWebSocket):

    node_address = None
    ssl_mode = None
    _batch_id = None

    def __init__(self, node_address, ssl_mode, batch_id):
        super(BaseTransactionResponse, self).__init__(node_address, ssl_mode)
        self._batch_id = batch_id
        self.data = {
            "batch_ids": [
                self._batch_id
            ]
        }

    @property
    def batch_id(self):
        try:
            return self.data["batch_ids"][0]
        except Exception:
            return None

    async def __aenter__(self):
        return await super().__aenter__()

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await super().__aexit__(exc_type, exc_val, exc_tb)
