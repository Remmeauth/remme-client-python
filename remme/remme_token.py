from remme.constants.remme_family_name import RemmeFamilyName
from remme.constants.remme_methods import RemmeMethods
from remme.protos.account_pb2 import AccountMethod, TransferPayload
from remme.protos.transaction_pb2 import TransactionPayload


class RemmeToken:

    api = None
    transaction_service = None
    _family_version = "0.1"

    def __init__(self, rest, transaction_service):
        self.api = rest
        self.transaction_service = transaction_service

    def validate_amount(self, amount):
        if amount <= 0:
            raise Exception("Invalid amount")
        return amount

    @staticmethod
    def validate_public_key(key):
        if len(key) != 66:
            raise Exception("Invalid key")
        return key

    @staticmethod
    def validate_public_key_address(address):
        if len(address) != 70:
            raise Exception("Invalid address")
        return address

    async def _create_transfer_tx(self, address, amount):
        receiver_address = self.validate_public_key_address(address=address)
        amount = self.validate_amount(amount)

        transfer = TransferPayload()
        transfer.address_to = receiver_address
        transfer.value = amount

        tr = TransactionPayload()
        tr.method = AccountMethod.TRANSFER
        tr.data = transfer.SerializeToString()

        return await self.transaction_service.create(
            family_name=RemmeFamilyName.ACCOUNT.value,
            family_version=self._family_version,
            inputs=[receiver_address],
            outputs=[receiver_address],
            payload_bytes=tr.SerializeToString(),
        )

    async def transfer(self, receiver_address, amount):
        receiver_address = self.validate_public_key_address(address=receiver_address)
        payload = await self._create_transfer_tx(receiver_address, amount)
        return await self.transaction_service.send(payload)

    async def get_balance(self, public_key_address):
        address = self.validate_public_key_address(address=public_key_address)
        params = {'public_key_address': address}
        result = await self.api.send_request(RemmeMethods.TOKEN, params)
        return result
