from remme.remmetoken import RemmeToken

__author__ = 'dethline'


class RemmeClient:

    token = None
    private_key_hex = None
    network_config = None

    def __init__(self, private_key_hex="", network_config=None):
        self.private_key_hex = private_key_hex
        if network_config is None:
            network_config = {'node_address': "localhost", 'node_port': "8080", 'ssl_mode': False}
        self.network_config = network_config
        self.token = RemmeToken(network_config=self.network_config)
