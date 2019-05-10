import base64

from sawtooth_sdk.protobuf.setting_pb2 import Setting

from remme.models.general.methods import RemmeMethods
from remme.models.interfaces.node_management import IRemmeNodeManagement
from remme.models.node_management.bet_type import BetType
from remme.models.node_management.node_account import NodeAccount
from remme.models.node_management.node_account_state import NodeAccountState
from remme.models.node_management.node_config import NodeConfig
from remme.models.node_management.node_info import NodeInfo
from remme.models.utils.constants import CONSENSUS_ADDRESS
from remme.models.utils.family_name import RemmeFamilyName
from remme.protobuf.node_account_pb2 import (
    NodeAccountInternalTransferPayload,
    NodeAccountMethod,
    SetBetPayload,
)
from remme.protobuf.transaction_pb2 import (
    EmptyPayload,
    TransactionPayload,
)
from remme.utils import generate_settings_address


class RemmeNodeManagement(IRemmeNodeManagement):
    """
    Class for working with node management.
    """

    _stake_settings_address = generate_settings_address(key='remme.settings.minimum_stake')
    _genesis_owners_address = generate_settings_address(key='remme.settings.genesis_owners')
    _master_node_list_address = '0' * 69 + '2'
    _family_name = RemmeFamilyName.NODE_ACCOUNT.value
    _family_version = '0.1'

    def __init__(self, remme_api, remme_account, remme_transaction):
        """
        Args:
            remme_api: RemmeAPI
            remme_account: RemmeAccount
            remme_transaction: RemmeTransactionService

        To use:
            Usage without remme main package.

            .. code-block:: python

                api = RemmeAPI()
                account = RemmeAccount()
                transaction = RemmeTransactionService()
        """
        self._remme_api = remme_api
        self._remme_account = remme_account
        self._remme_transaction = remme_transaction

    async def _check_node(self):
        node_account = await self.get_node_account()

        node_state = node_account.state

        if node_state != NodeAccountState.NEW.value:
            raise Exception(f'Master Node is already {node_state}.')

    async def _check_amount(self, amount):
        if not amount:
            raise Exception('Initial stake was not provided, please set the initial stake amount.')

        initial_stake = await self.get_initial_stake()

        if amount < initial_stake:
            raise Exception(f'Value for initialize Master Node is lower than {initial_stake}.')

    async def _create_and_send_transaction(self, method, data, inputs, outputs):
        transaction_payload = TransactionPayload(method=method, data=data).SerializeToString()

        transaction = await self._remme_transaction.create(
            family_name=self._family_name,
            family_version=self._family_version,
            inputs=inputs,
            outputs=outputs,
            payload_bytes=transaction_payload,
        )

        return await self._remme_transaction.send(payload=transaction)

    async def open_node(self):
        """
        Open node.

        To use:
            .. code-block:: python

                open_node = await remme.node_management.open_node()
        """
        open_node_payload = EmptyPayload().SerializeToString()

        inputs_and_outputs = []

        return await self._create_and_send_transaction(
            method=NodeAccountMethod.INITIALIZE_NODE,
            data=open_node_payload,
            inputs=inputs_and_outputs,
            outputs=inputs_and_outputs,
        )

    async def open_master_node(self, amount):
        """
        Open master node by amount.

        Args:
            amount (integer): amount of stake.

        To use:
            .. code-block:: python

                open_master_node = await remme.node_management.open_master_node(amount=250001)
        """
        if self._remme_account.family_name != self._family_name:
            raise Exception(
                f'This operation is allowed under NodeAccount. '
                f'Your account type is {self._remme_account.family_name} '
                f'and address is: {self._remme_account.address}.',
            )

        await self._check_node()
        await self._check_amount(amount=amount)

        open_master_node_payload = NodeAccountInternalTransferPayload(value=amount).SerializeToString()

        inputs_and_outputs = [
            self._master_node_list_address,
            self._stake_settings_address,
            CONSENSUS_ADDRESS,
        ]

        return await self._create_and_send_transaction(
            method=NodeAccountMethod.INITIALIZE_MASTERNODE,
            data=open_master_node_payload,
            inputs=inputs_and_outputs,
            outputs=inputs_and_outputs,
        )

    async def close_master_node(self):
        """
        Close master node.

        To use:
            .. code-block:: python

                close_master_node = await remme.node_management.close_master_node()
        """
        if self._remme_account.family_name != self._family_name:
            raise Exception(
                f'This operation is allowed under NodeAccount. '
                f'Your account type is {self._remme_account.family_name} '
                f'and address is: {self._remme_account.address}.',
            )

        close_payload = EmptyPayload().SerializeToString()

        inputs = [
            self._master_node_list_address,
            self._genesis_owners_address,
            CONSENSUS_ADDRESS,
        ]

        outputs = [
            self._master_node_list_address,
            CONSENSUS_ADDRESS,
        ]

        return await self._create_and_send_transaction(
            method=NodeAccountMethod.CLOSE_MASTERNODE,
            data=close_payload,
            inputs=inputs,
            outputs=outputs,
        )

    async def set_bet(self, bet_type):
        """
        Set bet by bet type (fixed_amount, max, min).

        Args:
            bet_type (string or integer): fixed_amount, max, min

        To use:
            .. code-block:: python

                set_bet = await remme.node_management.set_bet(1)
                set_bet = await remme.node_management.set_bet('MAX')
        """
        if self._remme_account.family_name != self._family_name:
            raise Exception(
                f'This operation is allowed under NodeAccount. '
                f'Your account type is {self._remme_account.family_name} '
                f'and address is: {self._remme_account.address}.',
            )

        bet = {}

        if isinstance(bet_type, int):
            bet['fixed_amount'] = bet_type

        elif bet_type == BetType.MAX.value or bet_type == BetType.MIN.value:
            bet[bet_type.lower()] = True

        else:
            raise Exception('Unknown betting behaviour.')

        bet_payload = SetBetPayload(**bet).SerializeToString()

        inputs_and_outputs = [CONSENSUS_ADDRESS]

        return await self._create_and_send_transaction(
            method=NodeAccountMethod.SET_BET,
            data=bet_payload,
            inputs=inputs_and_outputs,
            outputs=inputs_and_outputs,
        )

    async def get_initial_stake(self):
        """
        Get initial stake of node.

        To use:
            .. code-block:: python

                initial_stake = await remme.node_management.get_initial_stake()
        """
        data = await self._remme_api.send_request(
            method=RemmeMethods.FETCH_STATE,
            params={
                'address': self._stake_settings_address,
            },
        )

        setting = Setting()
        setting.ParseFromString(base64.b64decode(data.get('data')))

        value = setting.entries[0].value

        return int(value, 10)

    async def get_node_account(self, node_account_address=None):
        """
        Get node account by node account address.

        Args:
            node_account_address (string): node account address

        To use:
            .. code-block:: python

                node_account = await remme.node_management.get_node_account(
                    node_account_address='116829be95c8bb240396446ec359d0d7f04d257b72aeb4ab1ecfe50cf36e400a96ab9c',
                )
        """
        node_account_address = node_account_address if node_account_address else self._remme_account.address

        data = await self._remme_api.send_request(
            method=RemmeMethods.NODE_ACCOUNT,
            params={
                'node_account_address': node_account_address,
            }
        )
        return NodeAccount(node_account_response=data)

    async def get_node_info(self):
        """
        Get information about node.

        To use:
            .. code-block:: python

                node_info = await remme.node_management.get_node_info()
        """
        api_result = await self._remme_api.send_request(method=RemmeMethods.NETWORK_STATUS)
        return NodeInfo(data=api_result)

    async def get_node_config(self):
        """
        Get node config.

        To use:
            .. code-block:: python

                node_config = await remme.node_management.get_node_config()
        """
        api_result = await self._remme_api.send_request(method=RemmeMethods.NODE_CONFIG)
        return NodeConfig(data=api_result)
