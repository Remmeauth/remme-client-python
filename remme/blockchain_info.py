import base64
import re

from remme import protobuf
from remme.models.blockchain_info.block_info import BlockInfo
from remme.models.blockchain_info.network_status import NetworkStatus
from remme.models.blockchain_info.query import (
    BatchQuery,
    BlockQuery,
    StateQuery,
    TransactionQuery,
)
from remme.models.general.methods import RemmeMethods
from remme.models.general.patterns import RemmePatterns
from remme.models.interfaces.blockchain_info import IRemmeBlockchainInfo
from remme.models.utils import (
    RemmeFamilyName,
    RemmeNamespace,
)
from remme.utils import get_namespace_params


class RemmeBlockchainInfo(IRemmeBlockchainInfo):
    """
    Main class that works with blockchain data (blocks, batches, transactions, addresses, peers).
    """

    _address = {
        RemmeNamespace.SWAP.value: get_namespace_params(
            type='info atomic swap', parser=protobuf.AtomicSwapInfo(),
        ),
        RemmeNamespace.ACCOUNT.value: get_namespace_params(
            type='account', parser=protobuf.Account(),
        ),
        RemmeNamespace.NODE_ACCOUNT.value: get_namespace_params(
            type='node account', parser=protobuf.NodeAccount(),
        ),
        RemmeNamespace.PUBLIC_KEY.value: get_namespace_params(
            type='storage public key', parser=protobuf.PubKeyStorage(),
        ),
    }

    _correspond = {
        RemmeFamilyName.ACCOUNT.value: {
            protobuf.AccountMethod.TRANSFER: get_namespace_params(
                type='transfer token', parser=protobuf.TransferPayload(),
            ),
            protobuf.AccountMethod.GENESIS: get_namespace_params(
                type='genesis', parser=protobuf.GenesisPayload(),
            ),
        },
        RemmeFamilyName.NODE_ACCOUNT.value: {
            protobuf.NodeAccountMethod.INITIALIZE_MASTERNODE: get_namespace_params(
                type='initialize masternode',
                parser=protobuf.NodeAccountInternalTransferPayload(),
            ),
            protobuf.NodeAccountMethod.INITIALIZE_NODE: get_namespace_params(
                type='initialize node',
                parser=protobuf.EmptyPayload(),
            ),
            protobuf.NodeAccountMethod.CLOSE_MASTERNODE: get_namespace_params(
                type='close masternode',
                parser=protobuf.EmptyPayload(),
            ),
            protobuf.NodeAccountMethod.SET_BET: get_namespace_params(
                type='set bet',
                parser=protobuf.SetBetPayload(),
            ),
            protobuf.NodeAccountMethod.TRANSFER_FROM_FROZEN_TO_UNFROZEN: get_namespace_params(
                type='transfer from frozen to unfrozen',
                parser=protobuf.EmptyPayload(),
            ),
            protobuf.NodeAccountMethod.TRANSFER_FROM_UNFROZEN_TO_OPERATIONAL: get_namespace_params(
                type='transfer from unfrozen to operational',
                parser=protobuf.NodeAccountInternalTransferPayload(),
            ),
        },
        RemmeFamilyName.SWAP.value: {
            protobuf.AtomicSwapMethod.INIT: get_namespace_params(
                type='atomic-swap-init', parser=protobuf.AtomicSwapInitPayload(),
            ),
            protobuf.AtomicSwapMethod.APPROVE: get_namespace_params(
                type='atomic-swap-approve', parser=protobuf.AtomicSwapApprovePayload(),
            ),
            protobuf.AtomicSwapMethod.EXPIRE: get_namespace_params(
                type='atomic-swap-expire', parser=protobuf.AtomicSwapExpirePayload(),
            ),
            protobuf.AtomicSwapMethod.SET_SECRET_LOCK: get_namespace_params(
                type='atomic-swap-set-secret-lock', parser=protobuf.AtomicSwapSetSecretLockPayload(),
            ),
            protobuf.AtomicSwapMethod.CLOSE: get_namespace_params(
                type='atomic-swap-close', parser=protobuf.AtomicSwapClosePayload(),
            ),
        },
        RemmeFamilyName.PUBLIC_KEY.value: {
            protobuf.PubKeyMethod.STORE: get_namespace_params(
                type='store public key', parser=protobuf.NewPubKeyPayload(),
            ),
            protobuf.PubKeyMethod.REVOKE: get_namespace_params(
                type='revoke public key', parser=protobuf.RevokePubKeyPayload(),
            ),
        },
    }

    def __init__(self, remme_api):
        """
        Args:
            remme_api: RemmeAPI

        To use:
            Usage without remme main package.

            .. code-block:: python

                remme_api = RemmeAPI()
                remme_blockchain_info = RemmeBlockchainInfo(remme_api)
        """
        self._remme_api = remme_api

    @staticmethod
    def _check_id(id_):
        if id_ is None or re.match(RemmePatterns.HEADER_SIGNATURE.value, id_) is None:
            raise Exception('Given `id` is not a valid.')

    @staticmethod
    def _check_address(address):
        if address is None or re.match(RemmePatterns.ADDRESS.value, address) is None:
            raise Exception('Given `address` is not a valid.')

    async def get_blocks(self, query=None):
        """
        Get list of blocks from REMChain.
        You can specify one or more query parameters.

        Args:
            query (dict, optional): dictionary with specific parameters

        Returns:
            List of blocks.

        To use:
           Without query.

            .. code-block:: python

                blocks = await remme.blockchain_info.get_blocks()
                print(blocks)

           Start from specifying block number.

            .. code-block:: python

                blocks = await remme.blockchain_info.get_blocks({'start':4})
                print(blocks)

           Reverse output.

            .. code-block:: python

                blocks = await remme.blockchain_info.get_blocks({'reverse':'false'})
                print(blocks)

           Specify limit of output.

            .. code-block:: python

                blocks = await remme.blockchain_info.get_blocks({'limit':2})
                print(blocks)

           Specify head of block for start.

            .. code-block:: python

                head = '9d2dc2ab673d028bc1dd8b5be8d2d885e4383a827cd0261f58334252bf807c08' \
                    '113207eabbd12d0786d6bba5378a791129f9c520c17597b5504d4b547ef57491'
                blocks = await remme.blockchain_info.get_blocks({
                    'head': head
                })
                print(blocks)
        """
        if query:
            query = BlockQuery(query=query).get()

        return await self._remme_api.send_request(
            method=RemmeMethods.BLOCKS,
            params=query,
        )

    async def get_block_by_id(self, block_id):
        """
        Get block by id (header_signature) from REMChain.
        Specify limit of output.

        Args:
            block_id (string): block id

        Returns:
            Block.

        To use:
            .. code-block:: python

                id = '9d2dc2ab673d028bc1dd8b5be8d2d885e4383a827cd0261f58334252bf807c08' \
                    '113207eabbd12d0786d6bba5378a791129f9c520c17597b5504d4b547ef57491'
                block = await remme.blockchain_info.get_block_by_id(id)
                print(block)
        """
        self._check_id(id_=block_id)

        return await self._remme_api.send_request(
            method=RemmeMethods.FETCH_BLOCK,
            params={'id': block_id},
        )

    async def get_block_info(self, query=None):
        """
        Get information about block.

        Args:
            query (dict, optional): dictionary with specific parameters

        Returns:
            Information about block.

        To use:
          Without parameters.

            .. code-block:: python

                block_info = await remme.blockchain_info.get_block_info()
                print(block_info)

          Start from specifying block number.

            .. code-block:: python

                block_info = await remme.blockchain_info.get_block_info({'start':2})
                print(block_info)

          Specify limit of output.

            .. code-block:: python

                block_info = await remme.blockchain_info.get_block_info({'limit':2})
                print(block_info)
        """
        block_info = await self._remme_api.send_request(
            method=RemmeMethods.BLOCK_INFO,
            params=query,
        )

        if block_info is None:
            raise Exception('Unknown error occurs in the server.')

        empty_list_block = []

        if block_info == empty_list_block:
            return block_info

        return BlockInfo(data=block_info[0])

    async def get_batches(self, query=None):
        """
        Get list of batches from REMChain.

        Args:
            query (dict, optional): dictionary with specific parameters

        Returns:
            List of batches.

        To use:
           Without parameters.

            .. code-block:: python

                batches = await remme.blockchain_info.get_batches()
                print(batches)

           Start from specifying batch header_signature (batch ID).

            .. code-block:: python

                start = '8e4dc2ab673d028bc1dd8b5be8d2d885e4383a827cd0261f58334252bf807c08' \
                    '113207eabbd12d0786d6bba5378a791129f9c520c17597b5504d4b547ef5fe5c'
                batches = await remme.blockchain_info.get_batches({'start':start})
                print(batches)

           Reverse output.

            .. code-block:: python

                batches = await remme.blockchain_info.get_batches({'reverse':'false'})
                print(batches)

           Specify limit of output.

            .. code-block:: python

                batches = await remme.blockchain_info.get_batches({'limit':2})
                print(batches)

           Specify head of block for start.

            .. code-block:: python

                head = '9d2dc2ab673d028bc1dd8b5be8d2d885e4383a827cd0261f58334252bf807c08' \
                    '113207eabbd12d0786d6bba5378a791129f9c520c17597b5504d4b547ef57491'
                batches = await remme.blockchain_info.get_batches({'head':head})
                print(batches)
        """
        if query:
            query = BatchQuery(query=query).get()

        return await self._remme_api.send_request(
            method=RemmeMethods.BATCHES,
            params=query,
        )

    async def get_batch_by_id(self, batch_id):
        """
        Get batch by id (header_signature) from REMChain.

        Args:
            batch_id (string): header signature of transaction

        Returns:
            Batch.

        To use:
            .. code-block:: python

                id = '9d2dc2ab673d028bc1dd8b5be8d2d885e4383a827cd0261f58334252bf807c08' \
                    '113207eabbd12d0786d6bba5378a791129f9c520c17597b5504d4b547ef57491'
                batch = await remme.blockchain_info.get_batches_by_id(id)
                print(batch)
        """
        self._check_id(id_=batch_id)

        return await self._remme_api.send_request(
            method=RemmeMethods.FETCH_BATCH,
            params={'id': batch_id},
        )

    async def get_batch_status(self, batch_id):
        """
        Get status of batch.

        Args:
            batch_id (string): batch id

        Returns:
            Batch status.

        To use:
            .. code-block:: python

                id = '8e4dc2ab673d028bc1dd8b5be8d2d885e4383a827cd0261f58334252bf807c08' \
                    '113207eabbd12d0786d6bba5378a791129f9c520c17597b5504d4b547ef5fe5c'
                batch_status = await remme.blockchain_info.get_batch_status(id)
                print(batch_status)
        """
        self._check_id(id_=batch_id)

        return await self._remme_api.send_request(
            method=RemmeMethods.BATCH_STATUS,
            params={'id': batch_id},
        )

    async def get_states(self, query=None):
        """
        Get list of states in REMChain.

        Args:
            query (dict, optional): dictionary with specific parameters

        Returns:
            List of states.

        To use:
           Without parameters.

            .. code-block:: python

                states = await remme.blockchain_info.get_state()
                print(states)

           Start from specifying state address.

            .. code-block:: python

                states = await remme.blockchain_info.get_state({
                    'start':'6a437247a1c12c0fb03aa6e242e6ce988d1cdc7fcc8c2a62ab3ab1202325d7d677e84c'
                })
                print(states)

           Reverse output.

            .. code-block:: python

                states = await remme.blockchain_info.get_state({'reverse':'false'})
                print(states)

           Specify limit of output.

            .. code-block:: python

                states = await remme.blockchain_info.get_state({'limit':2})
                print(states)

           Specify head of block for start.

            .. code-block:: python

                head = 'f650727dad9a402656179904e95144b1ee1dd4b78a696a4d6d6122c82f5b78fe' \
                    '29c07d45d8842e435d2266e58a18c846137d351b840c4d6fed60b1b71edcb3c9'
                states = await remme.blockchain_info.get_state({'head':head})
                print(states)
        """
        if query:
            query = StateQuery(query=query).get()

        return await self._remme_api.send_request(
            method=RemmeMethods.STATE,
            params=query,
        )

    async def get_state_by_address(self, address):
        """
        Get state by address.

        Args:
            address (string): address

        Returns:
            State by giving address.

        To use:
            .. code-block:: python

                state = await remme.blockchain_info.get_state_by_address(
                    '6a437247a1c12c0fb03aa6e242e6ce988d1cdc7fcc8c2a62ab3ab1202325d7d677e84c'
                )
                print(state)
        """
        self._check_address(address=address)

        return await self._remme_api.send_request(
            method=RemmeMethods.FETCH_STATE,
            params={'address': address},
        )

    async def parse_state_data(self, state):
        """
        Parse state data.

        Args:
            state (dict): state data

        Returns:
            Parsed state.

        To use:
            .. code-block:: python

                state = await remme.blockchain_info.get_state_by_address(
                    '6a437247a1c12c0fb03aa6e242e6ce988d1cdc7fcc8c2a62ab3ab1202325d7d677e84c'
                )
                print(state)
                state['address'] = '6a437247a1c12c0fb03aa6e242e6ce988d1cdc7fcc8c2a62ab3ab1202325d7d677e84c'
                parsed_state = await remme.blockchain_info.parse_state_data(state)
                print(parsed_state)
        """
        address = state.get('address')

        if address is None:
            raise Exception('State should have address for parsing.')

        if not RemmeBlockchainInfo._address.get(address[0:6]):
            raise Exception(f'This address {address} don\'t supported for parsing.')

        namespace_params = RemmeBlockchainInfo._address.get(address[0:6])
        type_, parser = namespace_params.get('type'), namespace_params.get('parser')

        parser.ParseFromString(base64.b64decode(state.get('data')))

        return {
            'data': parser,
            'type': type_,
        }

    async def get_transactions(self, query=None):
        """
        Get list of transactions from REMChain.

        Args:
            query (dict, optional): dictionary with specific parameters

        Returns:
            List of transactions.

        To use:
           Without parameters.

            .. code-block:: python

                transactions = await remme.blockchain_info.get_transactions()
                print(transactions)

           Start from specifying transactions header_signature.

            .. code-block:: python

                start = 'f32fc2ab673d028bc1dd8b5be8d2d885e4383a827cd0261f58334252bf807c08' \
                    '113207eabbd12d0786d6bba5378a791129f9c520c17597b5504d4b547ef543fe'
                transactions = await remme.blockchain_info.get_transactions({'start':start})
                print(transactions)

           Reverse output.

            .. code-block:: python

                transactions = await remme.blockchain_info.get_transactions({'reverse':'false'})
                print(transactions)

           Specify limit of output.

            .. code-block:: python

                transactions = await remme.blockchain_info.get_transactions({'limit':2})
                print(transactions)

           Specify head of block for start.

            .. code-block:: python

                head = '9d2dc2ab673d028bc1dd8b5be8d2d885e4383a827cd0261f58334252bf807c08' \
                    '113207eabbd12d0786d6bba5378a791129f9c520c17597b5504d4b547ef57491'
                transactions = await remme.blockchain_info.get_transactions({'head':head})
                print(transactions)
        """
        if query:
            query = TransactionQuery(query=query).get()

        return await self._remme_api.send_request(
            method=RemmeMethods.TRANSACTIONS,
            params=query,
        )

    async def get_transaction_by_id(self, transaction_id):
        """
        Get transaction by id (header_signature) from REMChain.

        Args:
            transaction_id (string): header signature of transaction

        Returns:
            Transaction.

        To use:
            .. code-block:: python

                id = 'f32fc2ab673d028bc1dd8b5be8d2d885e4383a827cd0261f58334252bf807c08' \
                    '113207eabbd12d0786d6bba5378a791129f9c520c17597b5504d4b547ef543fe'
                transaction = await remme.blockchain_info.get_transaction_by_id(id)
                print(transaction)
        """
        self._check_id(id_=transaction_id)

        return await self._remme_api.send_request(
            method=RemmeMethods.FETCH_TRANSACTION,
            params={'id': transaction_id},
        )

    async def parse_transaction_payload(self, transaction):
        """
        Parse transaction payload. Take transaction and return object with payload and type.

        Args:
            transaction (dict): transaction payload

        Returns:
            Parsed transaction payload.

        To use:
            .. code-block:: python

                id = 'f32fc2ab673d028bc1dd8b5be8d2d885e4383a827cd0261f58334252bf807c08' \
                    '113207eabbd12d0786d6bba5378a791129f9c520c17597b5504d4b547ef543fe'
                transaction = await remme.blockchain_info.get_transaction_by_id(id)
                print(transaction)
                parsed_transaction = remme.blockchain_info.parse_transaction_payload(transaction.get('data'))
                print(parsed_transaction)
        """
        family_name = transaction.get('header').get('family_name')

        if family_name not in RemmeBlockchainInfo._correspond:
            raise Exception(f'Family name {family_name} don\'t supported for parsing.')

        payload = base64.b64decode(transaction.get('payload'))

        transaction_payload = protobuf.TransactionPayload()
        transaction_payload.ParseFromString(payload)

        method = transaction_payload.method
        data = transaction_payload.data

        namespace_params = RemmeBlockchainInfo._correspond.get(family_name).get(method)

        type_, parser = namespace_params.get('type'), namespace_params.get('parser')

        parser.ParseFromString(data)

        return {
            'payload': parser,
            'type': type_,
        }

    async def get_network_status(self):
        """
        Get network status for node.

        Returns:
            Network status.

        To use:
            .. code-block:: python

                network_status = await remme.blockchain_info.get_network_status()
                print(network_status)
        """
        network_status_data = await self._remme_api.send_request(method=RemmeMethods.NETWORK_STATUS)

        return NetworkStatus(data=network_status_data)

    async def get_peers(self):
        """
        Get peers that connected to this node.

        Returns:
            List of peers.

        To use:
            .. code-block:: python

                peers = await remme.blockchain_info.get_peers()
                print(peers)
        """
        return (await self._remme_api.send_request(method=RemmeMethods.PEERS)).get('data')

    async def get_receipts(self, ids):
        """
        Get list of transactions receipts.

        Args:
            ids (list): list of string

        Returns:
            List of transactions receipts.

        To use:
            .. code-block:: python

                ids = ['f32fc2ab673d028bc1dd8b5be8d2d885e4383a827cd0261f58334252bf807c08'
                       '113207eabbd12d0786d6bba5378a791129f9c520c17597b5504d4b547ef543fe']
                receipts = await remme.blockchain_info.get_receipts(ids)
                print(receipts)
        """
        for identifier in ids:
            self._check_id(id_=identifier)

        return (await self._remme_api.send_request(
            method=RemmeMethods.RECEIPTS, params={'ids': ids}
        )).get('data')
