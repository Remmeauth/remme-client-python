from random import random

from remme.utils import sha256_hexdigest


class JsonRpcRequest:
    """
    Class for generating a json rpc request.
    """

    id = sha256_hexdigest(float.hex(random() * 1000).lstrip('0x'))
    jsonrpc = '2.0'

    def __init__(self, method, params):
        self.method = method
        self.params = params

    def get_query(self):

        return {
            'jsonrpc': self.jsonrpc,
            'method': self.method,
            'params': self.params,
            'id': self.id,
        }
