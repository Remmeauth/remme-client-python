import base64

from sawtooth_sdk.protobuf.transaction_pb2 import (
    Transaction,
    TransactionHeader,
)
from remme.models.general.methods import RemmeMethods
from remme.models.interfaces.transaction_service import IRemmeTransactionService
from remme.models.transaction_service.base_transaction_response import BaseTransactionResponse
from remme.utils import (
    create_nonce,
    sha512_hexdigest,
)


class RemmeTransactionService(IRemmeTransactionService):
    """
    Class for creating and sending transactions.

    To use:
        .. code-block:: python

            remme = Remme()
            family_name = "pub_key"
            family_version = "0.1"
            inputs = outputs = []
            payload_bytes = b"serialized transaction"
            transaction = await remme.transaction.create(
                family_name, family_version, inputs, outputs, payload_bytes,
            )
            send_response = await remme.transaction.send(transaction)
    """

    def __init__(self, remme_api, remme_account):
        """
        Args:
            remme_api: RemmeAPI
            remme_account: RemmeAccount

        To use:
            Usage without main remme package.

            .. code-block:: python

                remme_api = RemmeAPI() # See RemmeAPI implementation
                remme_account = RemmeAccount() # See RemmeAccount implementation
                remme_transaction = RemmeTransactionService(remme_api, remmeAccount)
        """
        self._remme_account = remme_account
        self._remme_api = remme_api

    async def create(self, family_name, family_version, inputs, outputs, payload_bytes):
        """
        Create transactions.

        Args:
            family_name (string): enum RemmeFamilyName
            family_version (string): family version
            inputs (list): list of input address
            outputs (list): list of output address
            payload_bytes (bytes): payload bytes

        Returns:
            Transaction.

        References::
            Documentation for building transactions - https://bit.ly/2NrNbNi

        To use:
            .. code-block:: python

                family_name = "pub_key"
                family_version = "0.1"
                inputs = outputs = []
                payload_bytes = b"my transaction"
                transaction = await remme_transaction.create(
                    family_name, family_version, inputs, outputs, payload_bytes,
                )
        """
        node_config = await self._remme_api.send_request(method=RemmeMethods.NODE_CONFIG)
        batcher_public_key = node_config.get('node_public_key')

        transaction_header_bytes = TransactionHeader(
            family_name=family_name,
            family_version=family_version,
            inputs=inputs + [self._remme_account.address],
            outputs=outputs + [self._remme_account.address],
            signer_public_key=self._remme_account.public_key_hex,
            batcher_public_key=batcher_public_key,
            nonce=create_nonce(),
            dependencies=[],
            payload_sha512=sha512_hexdigest(payload_bytes)
        ).SerializeToString()

        signature = self._remme_account.sign(transaction_header_bytes)

        transaction = Transaction(
            header=transaction_header_bytes,
            header_signature=signature,
            payload=payload_bytes,
        ).SerializeToString()

        return base64.b64encode(transaction).decode('utf-8')

    async def send(self, payload):
        """
        Send transactions.

        Args:
            payload (bytes): transaction in base64

        Returns:
            Response.

        To use:
            .. code-block:: python

                send_response = await remme_transaction.send(transaction)
                print(send_request.batch_id)
        """
        batch_id = await self._remme_api.send_request(
            method=RemmeMethods.TRANSACTION,
            params={"data": payload},
        )

        return BaseTransactionResponse(
            network_config=self._remme_api.network_config,
            batch_id=batch_id,
        )
