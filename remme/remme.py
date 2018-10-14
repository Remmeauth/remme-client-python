from remme.remme_token import RemmeToken

__author__ = 'dethline'


class Remme:
    """
    Class representing a client for Remme.
    """

    token = None
    private_key_hex = None
    network_config = None

    def __init__(self, private_key_hex="", network_config=None):
        """
        :param private_key_hex: The hex of private key. Which is used for creating account in library
        which would sign transactions.
        :param network_config: The config of network.
        """
        self.private_key_hex = private_key_hex
        if network_config is None:
            network_config = {'node_address': "localhost", 'node_port': "8080", 'ssl_mode': False}
        self.network_config = network_config
        self.token = RemmeToken(network_config=self.network_config)
