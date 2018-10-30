from remme.remme_utils import create_nonce, sha512_hexdigest
from base64 import b64encode
from sawtooth_sdk.protobuf.transaction_pb2 import TransactionHeader, Transaction
from remme.remme_methods import RemmeMethods
from remme.models.base_transaction_response import BaseTransactionResponse


class RemmeTransactionService():

    _remme_api = None
    _remme_account = None

    def __init__(self, remme_api, remme_account):
        self._remme_account = remme_account
        self._remme_api = remme_api

    async def create(self, transaction_d_to):
        batcher_public_key = await self._remme_api.send_request(RemmeMethods.NODE_KEY)
        sender_address = self._remme_account.address
        txn_header_bytes = TransactionHeader(
            family_name=transaction_d_to.family_name,
            family_version=transaction_d_to.family_version,
            inputs=[sender_address] + transaction_d_to.inputs,
            outputs=[sender_address] + transaction_d_to.outputs,
            signer_public_key=self._remme_account.public_key_hex,
            batcher_public_key=batcher_public_key,
            nonce=create_nonce(),
            dependencies=[],
            payload_sha512=sha512_hexdigest(transaction_d_to.payload_bytes)
        ).SerializeToString()
        # print(f"tx_header_bytes : {txn_header_bytes}")
        signature = self._remme_account.sign(txn_header_bytes)
        print(f"tx signature : {signature}")
        is_valid = self._remme_account.verify(signature, txn_header_bytes)
        print(f"tx is valid ? - {is_valid}")
        txn = Transaction(
            header=txn_header_bytes,
            header_signature=signature,
            payload=transaction_d_to.payload_bytes
        )
        # print(f"transaction : {txn}")
        return b64encode(txn.SerializeToString()).decode('utf-8')

    async def send(self, payload):
        params = {"data": payload}
        batch_id = await self._remme_api.send_request(RemmeMethods.TRANSACTION, params)
        return BaseTransactionResponse(self._remme_api.node_address, self._remme_api.ssl_mode, batch_id)

