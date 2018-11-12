from remme.remme_utils import create_nonce, sha512_hexdigest
from base64 import b64encode
from sawtooth_sdk.protobuf.transaction_pb2 import TransactionHeader, Transaction
from remme.constants.remme_methods import RemmeMethods
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
        batcher_public_key = await self._remme_api.send_request(RemmeMethods.NODE_KEY)
        print(f"inputs {inputs + [self._remme_account.address]}")
        print(f"outputs {outputs + [self._remme_account.address]}")
        txn_header_bytes = TransactionHeader(
            family_name=family_name,
            family_version=family_version,
            # inputs=['a23be14ee9dee1f5d910903d35ea24ef43e4f11639ee69fd6f414f2e9c1c1aaf21d095',
            #         '0000007ca83d6bbb759da9cde0fb0dec1400c5482a777e854144e5e3b0c44298fc1c14',
            #         '0000007ca83d6bbb759da9ebbaccb7f4037885e3b0c44298fc1c14e3b0c44298fc1c14',
            #         '11200756d420660cfe7e32dc139cb3bdc90d09ef138704a9b4a9641cb3b74969c5089f',
            #         '1120077670ce6077a14293063cb64bf8eae38ab9c14c21880a9355862591d20a5a8566'],
            inputs=inputs + [self._remme_account.address],
            # outputs=['a23be14ee9dee1f5d910903d35ea24ef43e4f11639ee69fd6f414f2e9c1c1aaf21d095',
            #          '0000007ca83d6bbb759da9cde0fb0dec1400c5482a777e854144e5e3b0c44298fc1c14',
            #          '0000007ca83d6bbb759da9ebbaccb7f4037885e3b0c44298fc1c14e3b0c44298fc1c14',
            #          '11200756d420660cfe7e32dc139cb3bdc90d09ef138704a9b4a9641cb3b74969c5089f',
            #          '1120077670ce6077a14293063cb64bf8eae38ab9c14c21880a9355862591d20a5a8566'],
            outputs=outputs + [self._remme_account.address],
            signer_public_key=self._remme_account.public_key_hex,
            batcher_public_key=batcher_public_key,
            nonce=create_nonce(),
            dependencies=[],
            payload_sha512=sha512_hexdigest(payload_bytes)
        ).SerializeToString()
        signature = self._remme_account.sign(txn_header_bytes)
        txn = Transaction(
            header=txn_header_bytes,
            header_signature=signature,
            payload=payload_bytes
        ).SerializeToString()
        return b64encode(txn).decode('utf-8')

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
        params = {"data": payload}
        batch_id = await self._remme_api.send_request(RemmeMethods.TRANSACTION, params)
        return BaseTransactionResponse(self._remme_api.node_address, self._remme_api.ssl_mode, batch_id)
