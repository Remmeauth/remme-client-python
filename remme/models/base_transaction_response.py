from remme.remme_websocket import RemmeWebSocket


class BaseTransactionResponse(RemmeWebSocket):

    node_address = None
    ssl_mode = None
    batch_id = None

    def __init__(self, node_address, ssl_mode, batch_id):
        super(BaseTransactionResponse, self).__init__(node_address, ssl_mode)
        self.batch_id = batch_id
        self.data = {
            "batch_id": [
                self.batch_id
            ]
        }
