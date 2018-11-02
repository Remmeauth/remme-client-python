from remme.remme_websocket import RemmeWebSocket


class BaseTransactionResponse(RemmeWebSocket):

    node_address = None
    ssl_mode = None
    batch_id = None

    def __init__(self, node_address, ssl_mode, batch_id):
        super(BaseTransactionResponse, self).__init__(node_address, ssl_mode)
        self._batch_id = batch_id
        self.data = {
            "batch_id": [
                self._batch_id
            ]
        }
        print("base transaction response", self)

    async def __aenter__(self):
        return await super().__aenter__()

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await super().__aexit__(exc_type, exc_val, exc_tb)
