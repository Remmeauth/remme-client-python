from remme.constants.remme_family_name import RemmeFamilyName
from remme.constants.remme_methods import RemmeMethods
from remme.protos.account_pb2 import AccountMethod, TransferPayload
from remme.protos.transaction_pb2 import TransactionPayload
from remme.remme_utils import (
    is_address_valid,
    is_amount_valid,
)


class RemmeToken:

    _family_name = RemmeFamilyName.ACCOUNT.value
    _family_version = '0.1'

    def __init__(self, api, transaction_service):
        self.api = api
        self.transaction_service = transaction_service

        self.transfer_payload = TransferPayload()
        self.transaction_payload = TransactionPayload()

    async def get_balance(self, address):
        """
        Get token balance by address.
        """
        address_is_valid, error = is_address_valid(address=address)

        if not address_is_valid:
            raise Exception(error)

        return await self.api.send_request(method=RemmeMethods.TOKEN, params={
            'public_key_address': address,
        })

    async def transfer(self, address_to, amount):
        """
        Send transaction by receiver address and amount.
        """
        address_is_valid, error = is_address_valid(address=address_to)

        if not address_is_valid:
            raise Exception(error)

        amount_is_valid, error = is_amount_valid(amount=amount)

        if not address_is_valid:
            raise Exception(error)

        payload = await self._create_transaction(address_to=address_to, amount=amount)

        return await self.transaction_service.send(payload=payload)

    async def _create_transaction(self, address_to, amount):
        """
        Create transaction by receiver address and amount.
        """
        self.transfer_payload.address_to = address_to
        self.transfer_payload.value = amount

        self.transaction_payload.method = AccountMethod.TRANSFER
        self.transaction_payload.data = self.transfer_payload.SerializeToString()

        return await self.transaction_service.create(
            family_name=self._family_name,
            family_version=self._family_version,
            inputs=[address_to],
            outputs=[address_to],
            payload_bytes=self.transaction_payload.SerializeToString(),
        )
