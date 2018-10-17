from remme.remme_atomic_swap import RemmeSwap
from remme.remme_batch import RemmeBatch
from remme.remme_blockchain_info import RemmeBlockchainInfo
from remme.remme_certificate import RemmeCertificate
from remme.remme_token import RemmeToken
from remme.remme_account import RemmeAccount
from remme.remme_rest import RemmeRest
from remme.remme_transaction_service import RemmeTransactionService
from remme.remme_public_key_storage import RemmePublicKeyStorage
from remme.remme_websocket_events import RemmeWebSocketEvents

__author__ = 'dethline'


class Remme:
    """
    Class representing a client for Remme.
    """

    _private_key_hex = None
    _network_config = None
    _rest = None
    _account = None
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
        :param private_key_hex: The hex of private key. Which is used for creating account in library
        which would sign transactions.
        :param network_config: The config of network.
        """
        default_network_config = {'node_address': "localhost", 'node_port': "8080", 'ssl_mode': False}
        self._private_key_hex = private_key_hex
        self._network_config = default_network_config if network_config is None else network_config

        self._rest = RemmeRest(self._network_config)
        self._account = RemmeAccount(self._private_key_hex)

        self.transaction_service = RemmeTransactionService(self._rest, self._account)
        self.public_key_storage = RemmePublicKeyStorage(self._rest, self.transaction_service, self._account)
        self.certificate = RemmeCertificate(self.public_key_storage)
        self.token = RemmeToken(self._rest, self.transaction_service)
        self.batch = RemmeBatch(self._rest)
        self.swap = RemmeSwap(self._rest, self.transaction_service)
        self.blockchain_info = RemmeBlockchainInfo(self._rest)
        self.events = RemmeWebSocketEvents(self._rest.get_node_socket(), self._rest.get_ssl_mode())



