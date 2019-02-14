from remme.account import RemmeAccount
from remme.api import RemmeAPI
from remme.atomic_swap import RemmeSwap
from remme.blockchain_info import RemmeBlockchainInfo
from remme.certificate import RemmeCertificate
from remme.keys import RemmeKeys
from remme.public_key_storage import RemmePublicKeyStorage
from remme.token import RemmeToken
from remme.transaction_service import RemmeTransactionService
from remme.websocket_events import RemmeWebSocketEvents

DEFAULT_NETWORK_CONFIG = {
    'node_address': "localhost",
    'node_port': "8080",
    'ssl_mode': False,
}


class Remme:
    """
    Class representing a client for Remme.
    """

    def __init__(self, private_key_hex="", network_config=None):
        """
        :param private_key_hex: hex of private key, which is used for creating account in library
        which would sign transactions.
        :param network_config: config of network.
        """
        self._private_key_hex = private_key_hex
        self._network_config = DEFAULT_NETWORK_CONFIG if network_config is None else network_config

        self._api = RemmeAPI(self._network_config)
        self.account = RemmeAccount(self._private_key_hex)
        self.keys = RemmeKeys()

        self.transaction_service = RemmeTransactionService(self._api, self.account)
        self.public_key_storage = RemmePublicKeyStorage(self._api, self.account, self.transaction_service)
        self.certificate = RemmeCertificate(self.public_key_storage)
        self.token = RemmeToken(self._api, self.transaction_service)
        self.swap = RemmeSwap(self._api, self.transaction_service)
        self.blockchain_info = RemmeBlockchainInfo(self._api)
        self.events = RemmeWebSocketEvents(self._api.node_address, self._api.ssl_mode)
