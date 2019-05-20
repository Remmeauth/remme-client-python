from remme.models.general.methods import RemmeMethods
from remme.models.interfaces.token import IRemmeToken
from remme.models.utils.constants import (
    BLOCK_INFO_CONFIG_ADDRESS,
    BLOCK_INFO_NAMESPACE_ADDRESS,
    CONSENSUS_ADDRESS,
)
from remme.models.utils.family_name import RemmeFamilyName
from remme.protobuf.account_pb2 import (
    AccountMethod,
    TransferPayload,
)
from remme.protobuf.node_account_pb2 import (
    NodeAccountMethod,
    NodeAccountInternalTransferPayload,
)
from remme.protobuf.transaction_pb2 import (
    TransactionPayload,
    EmptyPayload,
)
from remme.utils import (
    generate_settings_address,
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

    _account_family_name = RemmeFamilyName.ACCOUNT.value
    _node_family_name = RemmeFamilyName.NODE_ACCOUNT.value
    _family_version = '0.1'
    _stake_settings_address = generate_settings_address(key='remme.settings.minimum_stake')

    def __init__(self, remme_api, remme_transaction, remme_account):
        """
        Args:
            remme_api: RemmeAPI
            remme_transaction: RemmeTransactionService
            remme_account: RemmeAccount

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
        self._remme_account = remme_account

        self.transfer_payload = TransferPayload()
        self.node_account_internal_transfer_payload = NodeAccountInternalTransferPayload()
        self.empty_payload = EmptyPayload()
        self.transaction_payload = TransactionPayload()

    async def _generate_and_send_transfer_payload(
            self, transfer_method, family_name, transfer_payload, inputs_outputs,
    ):
        self.transaction_payload.method = transfer_method
        self.transaction_payload.data = transfer_payload

        payload = await self._remme_transaction.create(
            family_name=family_name,
            family_version=self._family_version,
            inputs=inputs_outputs,
            outputs=inputs_outputs,
            payload_bytes=self.transaction_payload.SerializeToString(),
        )

        return await self._remme_transaction.send(payload=payload)

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

        if self._remme_account.family_name == self._node_family_name:
            self.transfer_payload.sender_account_type = TransferPayload.SenderAccountType.Value('NODE_ACCOUNT')
        else:
            self.transfer_payload.sender_account_type = TransferPayload.SenderAccountType.Value('ACCOUNT')

        inputs_outputs = [
            address_to,
            CONSENSUS_ADDRESS,
        ]

        return await self._generate_and_send_transfer_payload(
            transfer_method=AccountMethod.TRANSFER,
            family_name=self._account_family_name,
            transfer_payload=self.transfer_payload.SerializeToString(),
            inputs_outputs=inputs_outputs,
        )

    async def transfer_from_unfrozen_to_operational(self, amount):
        """
        Transfer tokens from unfrozen to operational address.
        Send transaction to REMChain.

        Args:
            amount (integer): amount of tokens

        Returns:
            Transaction result.

        To use:
            .. code-block:: python

                transaction_result = await remme.token.transfer_from_unfrozen_to_operational(10)
                print(f'Sending tokens...BatchId: {transaction_result.batch_id}')
        """
        if self._remme_account.family_name != self._node_family_name:
            raise Exception(
                f'This operation is allowed under NodeAccount. '
                f'Your account type is {self._remme_account.family_name} '
                f'and address is: {self._remme_account.address}.',
            )
        validate_amount(amount=amount)

        self.node_account_internal_transfer_payload.value = amount

        inputs_outputs = [CONSENSUS_ADDRESS]

        return await self._generate_and_send_transfer_payload(
            transfer_method=NodeAccountMethod.TRANSFER_FROM_UNFROZEN_TO_OPERATIONAL,
            family_name=self._node_family_name,
            transfer_payload=self.node_account_internal_transfer_payload.SerializeToString(),
            inputs_outputs=inputs_outputs,
        )

    async def transfer_from_frozen_to_unfrozen(self):
        """
        Transfer tokens from frozen to unfrozen address.
        Send transaction to REMChain.

        Returns:
            Transaction result.

        To use:
            .. code-block:: python

                transaction_result = await remme.token.transfer_from_frozen_to_unfrozen()
                print(f'Sending tokens...BatchId: {transaction_result.batch_id}')
        """
        if self._remme_account.family_name != self._node_family_name:
            raise Exception(
                f'This operation is allowed under NodeAccount. '
                f'Your account type is {self._remme_account.family_name} '
                f'and address is: {self._remme_account.address}.',
            )

        self.transaction_payload.method = NodeAccountMethod.TRANSFER_FROM_FROZEN_TO_UNFROZEN
        self.transaction_payload.data = self.empty_payload.SerializeToString()

        inputs_outputs = [
            CONSENSUS_ADDRESS,
            BLOCK_INFO_CONFIG_ADDRESS,
            BLOCK_INFO_NAMESPACE_ADDRESS,
            self._stake_settings_address,
        ]

        return await self._generate_and_send_transfer_payload(
            transfer_method=NodeAccountMethod.TRANSFER_FROM_FROZEN_TO_UNFROZEN,
            family_name=self._node_family_name,
            transfer_payload=self.empty_payload.SerializeToString(),
            inputs_outputs=inputs_outputs,
        )
