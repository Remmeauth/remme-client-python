from remme.remme_utils import create_nonce, sha512_hexdigest
from base64 import b64encode
from sawtooth_sdk.protobuf.transaction_pb2 import TransactionHeader, Transaction


class RemmeTransactionService:

    _remme_rest = None
    _remme_account = None

    def __init__(self, remme_rest, remme_account):
        self._remme_account = remme_account
        self._remme_rest = remme_rest

    async def create(self, family_name, family_version, inputs, outputs, payload_bytes):
        batcher_public_key = await self._remme_rest.send_rpc_request(self._remme_rest.methods.NODE_KEY)
        txn_header_bytes = TransactionHeader(
            family_name=family_name,
            family_version=family_version,
            inputs=inputs,
            outputs=outputs,
            signer_public_key=self._remme_account.get_public_key_hex(),
            batcher_public_key=batcher_public_key,
            nonce=create_nonce(),
            dependencies=[],
            payload_sha512=sha512_hexdigest(payload_bytes)
        ).SerializeToString()
        # print(f"tx_header_bytes : {txn_header_bytes}")
        signature = self._remme_account.sign(txn_header_bytes)
        # print(f"tx signature : {signature}")
        txn = Transaction(
            header=txn_header_bytes,
            header_signature=signature,
            payload=payload_bytes
        )
        # print(f"transaction : {txn}")
        return txn

    async def send(self, transaction):
        params = {"data": b64encode(transaction.SerializeToString()).decode('utf-8')}
        batch_id = await self._remme_rest.send_rpc_request(self._remme_rest.methods.TRANSACTION, params)
        print(f"batch id {batch_id}")
        return batch_id
