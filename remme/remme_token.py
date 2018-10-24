from remme.remme_utils import generate_address
from remme.protos.account_pb2 import AccountMethod, TransferPayload
from remme.protos.transaction_pb2 import TransactionPayload


class RemmeToken:

    rest = None
    transaction_service = None
    _family_name = "account"
    _family_version = "0.1"

    def __init__(self, rest, transaction_service):
        self.rest = rest
        self.transaction_service = transaction_service

    def validate_amount(self, amount):
        if amount <= 0:
            raise Exception("Invalid amount")
        return amount

    async def transfer(self, public_key_to, amount):
        public_key_to = self.validate_public_key(public_key_to)
        amount = self.validate_amount(amount)
        receiver_address = generate_address(self._family_name, public_key_to)
        print(f"receiver address: {receiver_address}")

        transfer = TransferPayload()
        transfer.address_to = receiver_address
        transfer.value = amount

        tr = TransactionPayload()
        tr.method = AccountMethod.TRANSFER
        tr.data = transfer.SerializeToString()

        transaction = await self.transaction_service.create(**{
            "family_name": self._family_name,
            "family_version": self._family_version,
            "inputs": receiver_address,
            "outputs": receiver_address,
            "payload_bytes": tr.SerializeToString()
        })
        return await self.transaction_service.send(transaction)

    def validate_public_key(self, key):
        if len(key) != 66:
            raise Exception("Invalid key")
        return key

    async def get_balance(self, public_key):
        result = await self.rest.get_balance(public_key=self.validate_public_key(public_key))
        print(f'get_balance result: {result}')
        return result
