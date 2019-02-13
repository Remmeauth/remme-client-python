from remme.remme_utils import create_nonce, sha512_hexdigest
import base64
from sawtooth_sdk.protobuf.transaction_pb2 import TransactionHeader, Transaction
from remme.enums.remme_methods import RemmeMethods
from remme.models.base_transaction_response import BaseTransactionResponse


class RemmeTransactionService:
    """
    Class for creating and sending transactions
    @example
    ```python
    remme = Remme()
    family_name = "pub_key"
    family_version = "0.1"
    inputs = []
    outputs = []
    payload_bytes = b"serialized transaction"
    transaction = await remme.transaction_service.create(family_name, family_version, inputs, outputs, payload_bytes)
    send_response = await remme.transaction_service.send(transaction)
    ```
    """

    _remme_api = None
    _remme_account = None

    def __init__(self, remme_api, remme_account):
        """
        @example
        Usage without remme main package
        ```python
        remme_api = RemmeApi() # See RemmeApi implementation
        remme_account = RemmeAccount() # See RemmeAccount implementation
        remme_transaction = RemmeTransactionService(remmeApi, remmeAccount)
        ```
        :param remme_api: {RemmeApi}
        :param remme_account: {RemmeAccount}
        """
        self._remme_account = remme_account
        self._remme_api = remme_api

    async def create(self, family_name, family_version, inputs, outputs, payload_bytes):
        """
        Documentation for building transactions
        https://sawtooth.hyperledger.org/docs/core/releases/latest/_autogen/sdk_submit_tutorial_python.html#building-the-transaction
        @example
        ```python
        family_name = "pub_key"
        family_version = "0.1"
        inputs = []
        outputs = []
        payload_bytes = b"my transaction"
        transaction = await remme_transaction.create(family_name, family_version, inputs, outputs, payload_bytes)
        ```
        :param family_name: {string}
        :param family_version: {string}
        :param inputs: {list}
        :param outputs: {list}
        :param payload_bytes: {bytes}
        :return: {Couroutine}
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
        @example
        ```python
        send_response = await remme_transaction.send(transaction)
        print(send_request.batch_id)
        ```
        :param payload: {string} transaction
        :return: {Couroutine}
        """
        batch_id = await self._remme_api.send_request(
            method=RemmeMethods.TRANSACTION,
            params={"data": payload},
        )

        return BaseTransactionResponse(
            node_address=self._remme_api.node_address,
            ssl_mode=self._remme_api.ssl_mode,
            batch_id=batch_id,
        )
