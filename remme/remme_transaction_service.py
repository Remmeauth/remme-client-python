from remme.remme_utils import create_nonce, sha512_hexdigest
from base64 import b64encode
from sawtooth_sdk.protobuf.transaction_pb2 import TransactionHeader, Transaction


class CreateTransactionDto:
    family_name = None
    family_version = None
    inputs = None
    outputs = None
    payload_bytes = None

    def __init__(self, family_name, family_version, inputs, outputs, payload_bytes):
        self.family_name = family_name
        self.family_version = family_version
        self.inputs = inputs
        self.outputs = outputs
        self.payload_bytes = payload_bytes


class RemmeTransactionService:

    _remme_rest = None
    _remme_account = None

    def __init__(self, remme_rest, remme_account):
        self._remme_account = remme_account
        self._remme_rest = remme_rest

    async def create(self, transaction_d_to):
        batcher_public_key = await self._remme_rest.send_rpc_request(self._remme_rest.methods.NODE_KEY)
        sender_address = self._remme_account.address
        txn_header_bytes = TransactionHeader(
            family_name=transaction_d_to.family_name,
            family_version=transaction_d_to.family_version,
            inputs=[sender_address] + transaction_d_to.inputs,
            outputs=[sender_address] + transaction_d_to.outputs,
            signer_public_key=self._remme_account.get_public_key_hex(),
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
        batch_id = await self._remme_rest.send_rpc_request(self._remme_rest.methods.TRANSACTION, params)
        return batch_id

