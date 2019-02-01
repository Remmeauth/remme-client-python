import re

from remme import protos
from remme.enums.remme_methods import RemmeMethods
from remme.enums.remme_patterns import RemmePatterns
from remme.remme_blockchain_info.interface import IRemmeBlockchainInfo
from remme.remme_blockchain_info.models.block_info import BlockInfo
from remme.remme_blockchain_info.models.network_status import NetworkStatus
from remme.remme_blockchain_info.models.query import BaseQuery
from remme.remme_utils.models import (
    RemmeFamilyName,
    RemmeNamespace,
)


class RemmeBlockchainInfo(IRemmeBlockchainInfo):
    """
    Main class that works with blockchain data (blocks, batches, transactions, addresses, peers).
    """

    def __init__(self, remme_api):
        """
        @example
        Usage without remme main package.
        ```python
        remme_api = RemmeAPI()
        remme_blockchain_info = RemmeBlockchainInfo(remme_api)
        ```
        :param remme_api: RemmeAPI
        """
        self._remme_api = remme_api

    @staticmethod
    def _check_id(id):
        if id is None or not (re.match(RemmePatterns.HEADER_SIGNATURE.value, id) is not None):
            raise Exception('Given `id` is not a valid.')

    @staticmethod
    def _check_address(address):
        if address is None or not (re.match(RemmePatterns.ADDRESS.value, address) is not None):
            raise Exception('Given `address` is not a valid.')

    def _get_address(self, namespace):
        if namespace == RemmeNamespace.SWAP.value:
            return {
                'type': 'info atomic swap',
                'parser': protos.AtomicSwapInfo,
            }

        if namespace == RemmeNamespace.ACCOUNT.value:
            return {
                'type': 'account',
                'parser': protos.Account,
            }

        if namespace == RemmeNamespace.PUBLIC_KEY.value:
            return {
                'type': 'storage public key',
                'parser': protos.PubKeyStorage,
            }

    def _correspond(self, family_name, method=None):

        if family_name == RemmeFamilyName.ACCOUNT.value:

            if method == protos.AccountMethod.TRANSFER:
                return {
                    'type': 'transfer token',
                    'parser': protos.TransferPayload,
                }
            if method == protos.AccountMethod.GENESIS:
                return {
                    'type': 'genesis',
                    'parser': protos.GenesisPayload,
                }

        if family_name == RemmeFamilyName.SWAP.value:

            if method == protos.AtomicSwapMethod.INIT:
                return {
                    'type': 'atomic-swap-init',
                    'parser': protos.AtomicSwapInitPayload,
                }
            if method == protos.AtomicSwapMethod.APPROVE:
                return {
                    'type': 'atomic-swap-approve',
                    'parser': protos.AtomicSwapApprovePayload,
                }
            if method == protos.AtomicSwapMethod.EXPIRE:
                return {
                    'type': 'atomic-swap-expire',
                    'parser': protos.AtomicSwapExpirePayload,
                }
            if method == protos.AtomicSwapMethod.SET_SECRET_LOCK:
                return {
                    'type': 'atomic-swap-set-secret-lock',
                    'parser': protos.AtomicSwapSetSecretLockPayload,
                }
            if method == protos.AtomicSwapMethod.CLOSE:
                return {
                    'type': 'atomic-swap-close',
                    'parser': protos.AtomicSwapClosePayload,
                }

        if family_name == RemmeFamilyName.PUBLIC_KEY.value:

            if method == protos.PubKeyMethod.STORE:
                return {
                    'type': 'store public key',
                    'parser': protos.NewPubKeyPayload,
                }
            if method == protos.PubKeyMethod.REVOKE:
                return {
                    'type': 'revoke public key',
                    'parser': protos.RevokePubKeyPayload,
                }


    async def get_blocks(self, query=None):
        """
        Get all blocks from REMChain.
        You can specify one or more query parameters.
        :param query:
        """
        if query is not None:
            if isinstance(query, int):
                query['start'] = f'0x("0000000000000000" + query.start.toString(16)).slice(-16)'
            query = BaseQuery(query=query)

        return await self._remme_api.send_request(
            method=RemmeMethods.BLOCKS,
            params=query,
        )

    async def get_block_by_id(self, id):
        """
        Get block by id (header_signature) from REMChain.
        :param id: string
        """
        self._check_id(id=id)

        return await self._remme_api.send_request(
            method=RemmeMethods.FETCH_BLOCK,
            params={'id': id},
        )

    async def get_block_info(self, query=None):
        """
        Get information about block.
        :param query:
        """
        blocks = self._remme_api.send_request(
            method=RemmeMethods.BLOCK_INFO,
            params=query,
        )

        if blocks is None:
            raise Exception('Unknown error occurs in the server.')

        return BlockInfo(data=blocks)

    async def get_batches(self, query=None):
        """
        Get all batches from REMChain.
        :param query:
        """
        if query is not None:
            query = BaseQuery(query=query)

        return await self._remme_api.send_request(
            method=RemmeMethods.BATCHES,
            params=query,
        )

    async def get_batches_by_id(self, id):
        """
        Get batch by id (header_signature) from REMChain.
        :param id: string
        """
        self._check_id(id=id)

        return await self._remme_api.send_request(
            method=RemmeMethods.FETCH_BATCH,
            params={'id': id},
        )

    async def get_batches_status(self, batch_id):
        """
        Get status of batch.
        :param batch_id: string
        """
        self._check_id(id=batch_id)

        return await self._remme_api.send_request(
            method=RemmeMethods.BATCH_STATUS,
            params={'id': batch_id},
        )

    async def get_state(self, query=None):
        """
        Get states in REMChain.
        :param query:
        """
        if query is not None:
            query = BaseQuery(query=query)

        return await self._remme_api.send_request(
            method=RemmeMethods.STATE,
            params=query,
        )

    async def get_state_by_address(self, address):
        """
        Get state by address.
        :param address: string
        """
        self._check_address(address=address)

        return await self._remme_api.send_request(
            method=RemmeMethods.FETCH_STATE,
            params={'address': address},
        )

    async def parse_state_data(self, state):
        """
        Parse state data.
        :param state:
        """
        if state.get('address') is None:
            raise Exception('State should have address for parsing.')

        raise Exception(f'This address {state.address} don\'t supported for parsing.')

    async def get_transactions(self, query=None):
        """
        Get all transactions from REMChain.
        :param query:
        """
        if query is not None:
            query = BaseQuery(query=query)

        return await self._remme_api.send_request(
            method=RemmeMethods.TRANSACTIONS,
            params=query,
        )

    async def get_transaction_by_id(self, id):
        """
        Get transaction by id (header_signature) from REMChain.
        :param id: string
        """
        self._check_id(id=id)

        return await self._remme_api.send_request(
            method=RemmeMethods.FETCH_TRANSACTION,
            params={'id': id},
        )

    async def parse_transaction_payload(self, transaction):
        """
        Parse transaction payload. Take transaction and return object with payload and type.
        :param transaction:
        """
        family_name = transaction.get('header')

        if family_name in self._correspond(family_name=family_name):

            parser = ''
            return {'payload':  1, 'type': 2}  # parser.decode(data)
        else:
            raise Exception(f'Family name {family_name} don\'t supported for parsing.')

    async def get_network_status(self):
        """
        Get network status for node.
        """
        network_status_data = await self._remme_api.send_request(method=RemmeMethods.NETWORK_STATUS)

        return NetworkStatus(network_status=network_status_data)

    async def get_peers(self):
        """
        Get peers that connected to this node.
        """
        return (await self._remme_api.send_request(method=RemmeMethods.PEERS)).data
