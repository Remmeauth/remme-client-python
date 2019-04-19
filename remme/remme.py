"""
Main namespace. Which include all interaction with our client for developers.
"""
from remme.account import (
    RemmeAccount,
    DEFAULT_ACCOUNT_CONFIG,
)
from remme.api import (
    RemmeAPI,
    DEFAULT_NETWORK_CONFIG,
)
from remme.atomic_swap import RemmeSwap
from remme.blockchain_info import RemmeBlockchainInfo
from remme.certificate import RemmeCertificate
from remme.keys import RemmeKeys
from remme.node_management import RemmeNodeManagement
from remme.public_key_storage import RemmePublicKeyStorage
from remme.token import RemmeToken
from remme.transaction_service import RemmeTransactionService
from remme.websocket_events import RemmeWebSocketEvents


class Remme:
    """
    Class representing a client for Remme.
    """

    keys = RemmeKeys()

    def __init__(self, account_config=DEFAULT_ACCOUNT_CONFIG, network_config=DEFAULT_NETWORK_CONFIG):
        """
        Args:
            account_config (dict): config of user account (private key hex and account type)
            network_config (dict): config of network (node address and ssl mode)
        """
        self.account_config = account_config
        self.network_config = network_config

        self._remme_api = RemmeAPI(self.network_config)
        self._account = RemmeAccount(**self.account_config)

        self.transaction = RemmeTransactionService(self._remme_api, self._account)
        self.public_key_storage = RemmePublicKeyStorage(self._remme_api, self._account, self.transaction)
        self.certificate = RemmeCertificate(self.public_key_storage)
        self.token = RemmeToken(self._remme_api, self.transaction, self._account)
        self.swap = RemmeSwap(self._remme_api, self.transaction)
        self.blockchain_info = RemmeBlockchainInfo(self._remme_api)
        self.node_management = RemmeNodeManagement(self._remme_api, self._account, self.transaction)

        self._events = RemmeWebSocketEvents(self._remme_api.network_config)

    @property
    def account(self):
        """
        Get information about current account.

        To use:
            .. code-block:: python

                print(remme.account)

            Provide an account which sign the transactions that send to our nodes.
            For account use ECDSA (secp256k1) key pair.

            .. code-block:: python

                account = Remme.generate_account()
                remme.account = account
        """
        return self._account

    @account.setter
    def account(self, remme_account):

        if not remme_account:
            raise Exception('Account is missing in attributes. Please give the account.')

        if not remme_account.private_key_hex or not remme_account.sign or not remme_account.public_key_hex:
            raise Exception('Given remme_account is not a valid.')

        self._account = remme_account

    @staticmethod
    def generate_account():
        """
        Generate a new account.

        To use:
            .. code-block:: python

                account = Remme.generate_account()
                print(account)
        """
        return RemmeAccount()

    @property
    def events(self):
        """
        This properties hold implementation of RemmeWebSocketEvents,
        which get a possibility to listen events from validator about transactions.

        To use:
            Subscribe to event.

            .. code-block:: python

                remme.events.subscribe(
                    events=RemmeEvents.AtomicSwap.value,
                    last_known_block_id=last_known_block_id  # also can be set if you know it
                )

            Unsubscribe.

            .. code-block:: python

                remme.events.unsubscribe()
        """
        return self._events
