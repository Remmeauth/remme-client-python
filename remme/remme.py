from remme.remme_account import RemmeAccount
from remme.remme_api import RemmeAPI
from remme.remme_atomic_swap.remme_atomic_swap import RemmeSwap
from remme.remme_batch import RemmeBatch
from remme.remme_blockchain_info import RemmeBlockchainInfo
from remme.remme_certificate import RemmeCertificate
from remme.remme_keys.remme_keys import RemmeKeys
from remme.remme_public_key_storage import RemmePublicKeyStorage
from remme.remme_token import RemmeToken
from remme.remme_transaction_service import RemmeTransactionService
from remme.remme_websocket_events.remme_websocket_events import RemmeWebSocketEvents

DEFAULT_NETWORK_CONFIG = {
    'node_address': "localhost",
    'node_port': "8080",
    'ssl_mode': False,
}


class Remme:
    """
    Class representing a client for Remme.
    """

    _private_key_hex = None
    _network_config = None
    _api = None
    account = None
    transaction_service = None
    public_key_storage = None
    certificate = None
    token = None
    batch = None
    swap = None
    blockchain_info = None
    events = None

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
        self.batch = RemmeBatch(self._api)
        self.swap = RemmeSwap(self._api, self.transaction_service)
        self.blockchain_info = RemmeBlockchainInfo(self._api)
        self.events = RemmeWebSocketEvents(self._api.node_address, self._api.ssl_mode)
