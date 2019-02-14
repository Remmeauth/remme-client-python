from remme.models.general.methods import RemmeMethods
from remme.models.utils.family_name import RemmeFamilyName
from remme.protobuf.account_pb2 import AccountMethod, TransferPayload
from remme.protobuf.transaction_pb2 import TransactionPayload
from remme.utils import (
    public_key_address,
    validate_address,
    validate_amount,
)


class RemmeToken:
    """
    Class that work with tokens. Transfer them and getting balance by address.

    @example
    ```python
    some_remme_address = '1120077f88b0b798347b3f52751bb99fa8cabaf926c5a1dad2d975d7b966a85b3a9c21'

    receiver_balance = await remme.token.get_balance(some_remme_address)
    print(f'Account {some_remme_address} as receiver, balance - {receiver_balance} REM')

    balance = await remme.token.get_balance(remme.account.address)
    print(f'Account {remme.account.address} as sender, balance - {balance} REM')

    transaction_result = await remme.token.transfer(some_remme_address, 10)
    print(f'Sending tokens...BatchId: {transaction_result.batch_id}')

    async for batch_info in transaction_result.connect_to_web_socket():
        if batch_info.status == BatchStatus.COMMITTED.value:
            new_balance = await remme.token.get_balance(some_remme_address)
            print(f'Account {some_remme_address} balance - {new_balance} REM')
            await transaction_result.close_web_socket()
    ```
    """

    _family_name = RemmeFamilyName.ACCOUNT.value
    _family_version = '0.1'

    def __init__(self, api, transaction_service):
        self.api = api
        self.transaction_service = transaction_service

        self.transfer_payload = TransferPayload()
        self.transaction_payload = TransactionPayload()

    async def get_balance(self, address):
        """
        Get balance on given account address.

        @example
        ```python
        balance = await remme.token.get_balance(remme.account.address)
        print(f'Account {remme.account.address} as sender, balance - {balance} REM')
        ```

        :param address: {string}
        :return: {integer}
        """
        validate_address(address=address)

        return await self.api.send_request(
            method=RemmeMethods.TOKEN,
            params=public_key_address(value=address),
        )

    async def transfer(self, address_to, amount):
        """
        Transfer tokens from signed address (remme.account.address) to given address.
        Send transaction to REMChain.

        @example
        ```python
        some_remme_address = '1120077f88b0b798347b3f52751bb99fa8cabaf926c5a1dad2d975d7b966a85b3a9c21'

        transaction_result = await remme.token.transfer(some_remme_address, 10)
        print(f'Sending tokens...BatchId: {transaction_result.batch_id}')

        async for batch_info in transaction_result.connect_to_web_socket():
            if batch_info.status == BatchStatus.COMMITTED.value:
                new_balance = await remme.token.get_balance(some_remme_address)
                print(f'Account {some_remme_address} balance - {new_balance} REM')
                await transaction_result.close_web_socket()
        ```

        :param address_to: {string}
        :param amount: {integer}
        :return: {string}
        """
        validate_address(address=address_to)
        validate_amount(amount=amount)

        self.transfer_payload.address_to = address_to
        self.transfer_payload.value = amount

        self.transaction_payload.method = AccountMethod.TRANSFER
        self.transaction_payload.data = self.transfer_payload.SerializeToString()

        payload = await self.transaction_service.create(
            family_name=self._family_name,
            family_version=self._family_version,
            inputs=[address_to],
            outputs=[address_to],
            payload_bytes=self.transaction_payload.SerializeToString(),
        )

        return await self.transaction_service.send(payload=payload)
