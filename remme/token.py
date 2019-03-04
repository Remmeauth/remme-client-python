from remme.models.general.methods import RemmeMethods
from remme.models.interfaces.token import IRemmeToken
from remme.models.utils.family_name import RemmeFamilyName
from remme.protobuf.account_pb2 import (
    AccountMethod,
    TransferPayload,
)
from remme.protobuf.transaction_pb2 import TransactionPayload
from remme.utils import (
    public_key_address,
    validate_address,
    validate_amount,
)


class RemmeToken(IRemmeToken):
    """
    Class that work with tokens. Transfer them and getting balance by address.

    To use:
        .. code-block:: python

            some_account_public_key_in_hex = '02926476095ea28904c11f22d0da20e999801a267cd3455a00570aa1153086eb13'
            some_remme_address = generate_address(
                RemmeFamilyName.ACCOUNT.value,
                some_account_public_key_in_hex,
            )

            receiver_balance = await remme.token.get_balance(some_remme_address)
            print(f'Account {some_remme_address} as receiver, balance - {receiver_balance} REM')

            balance = await remme.token.get_balance(remme.account.address)
            print(f'Account {remme.account.address} as sender, balance - {balance} REM')

            transaction_result = await remme.token.transfer(some_remme_address, 10)
            print(f'Sending tokens...Batch_id: {transaction_result.batch_id}')

            async for batch_info in transaction_result.connect_to_web_socket():
                if batch_info.status == BatchStatus.COMMITTED.value:
                    new_balance = await remme.token.get_balance(some_remme_address)
                    print(f'Account {some_remme_address} balance - {new_balance} REM')
                    await transaction_result.close_web_socket()
    """

    _family_name = RemmeFamilyName.ACCOUNT.value
    _family_version = '0.1'

    def __init__(self, remme_api, remme_transaction):
        """
        Args:
            remme_api: RemmeAPI
            remme_transaction: RemmeTransactionService

        To use:
            Usage without main remme package.

            .. code-block:: python

                remme_api = RemmeAPI() # See RemmeAPI implementation
                remme_account = RemmeAccount() # See RemmeAccount implementation
                remme_transaction = RemmeTransactionService(remme_api, remmeAccount)
                remme_token = RemmeToken(remme_api, remme_transaction)
        """
        self._remme_api = remme_api
        self._remme_transaction = remme_transaction

        self.transfer_payload = TransferPayload()
        self.transaction_payload = TransactionPayload()

    async def get_balance(self, address):
        """
        Get balance on given account address.

        Args:
            address (string): account address

        Returns:
            Balance.

        To use:
            .. code-block:: python

                balance = await remme.token.get_balance(remme.account.address)
                print(f'Account {remme.account.address} as sender, balance - {balance} REM.')
        """
        validate_address(address=address)

        return await self._remme_api.send_request(
            method=RemmeMethods.TOKEN,
            params=public_key_address(value=address),
        )

    async def transfer(self, address_to, amount):
        """
        Transfer tokens from signed address (remme.account.address) to given address.
        Send transaction to REMChain.

        Args:
            address_to (string): given address
            amount (integer): amount of tokens

        Returns:
            Transaction result.

        To use:
            .. code-block:: python

                some_account_public_key_in_hex = '02926476095ea28904c11f22d0da20e999801a267cd3455a00570aa1153086eb13'
                some_remme_address = generate_address(
                    RemmeFamilyName.ACCOUNT.value,
                    some_account_public_key_in_hex,
                )

                transaction_result = await remme.token.transfer(some_remme_address, 10)
                print(f'Sending tokens...BatchId: {transaction_result.batch_id}')

                async for batch_info in transaction_result.connect_to_web_socket():
                    if batch_info.status == BatchStatus.COMMITTED.value:
                        new_balance = await remme.token.get_balance(some_remme_address)
                        print(f'Account {some_remme_address} balance - {new_balance} REM')
                        await transaction_result.close_web_socket()
        """
        validate_address(address=address_to)
        validate_amount(amount=amount)

        self.transfer_payload.address_to = address_to
        self.transfer_payload.value = amount

        self.transaction_payload.method = AccountMethod.TRANSFER
        self.transaction_payload.data = self.transfer_payload.SerializeToString()

        payload = await self._remme_transaction.create(
            family_name=self._family_name,
            family_version=self._family_version,
            inputs=[address_to],
            outputs=[address_to],
            payload_bytes=self.transaction_payload.SerializeToString(),
        )

        return await self._remme_transaction.send(payload=payload)
