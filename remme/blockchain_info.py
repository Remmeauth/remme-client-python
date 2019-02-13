import base64
import re

from remme import protos
from remme.models.general.methods import RemmeMethods
from remme.models.general.patterns import RemmePatterns
from remme.interfaces.blockchain_info import IRemmeBlockchainInfo
from remme.models.blockchain_info.block_info import BlockInfo
from remme.models.blockchain_info.network_status import NetworkStatus
from remme.models.blockchain_info.query import (
    BaseQuery,
    StateQuery,
)
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
            type='info atomic swap', parser=protos.AtomicSwapInfo(),
        ),
        RemmeNamespace.ACCOUNT.value: get_namespace_params(
            type='account', parser=protos.Account(),
        ),
        RemmeNamespace.PUBLIC_KEY.value: get_namespace_params(
            type='storage public key', parser=protos.PubKeyStorage(),
        ),
    }

    _correspond = {
        RemmeFamilyName.ACCOUNT.value: {
            protos.AccountMethod.TRANSFER: get_namespace_params(
                type='transfer token', parser=protos.TransferPayload(),
            ),
            protos.AccountMethod.GENESIS: get_namespace_params(
                type='genesis', parser=protos.GenesisPayload(),
            ),
        },
        RemmeFamilyName.SWAP.value: {
            protos.AtomicSwapMethod.INIT: get_namespace_params(
                type='atomic-swap-init', parser=protos.AtomicSwapInitPayload(),
            ),
            protos.AtomicSwapMethod.APPROVE: get_namespace_params(
                type='atomic-swap-approve', parser=protos.AtomicSwapApprovePayload(),
            ),
            protos.AtomicSwapMethod.EXPIRE: get_namespace_params(
                type='atomic-swap-expire', parser=protos.AtomicSwapExpirePayload(),
            ),
            protos.AtomicSwapMethod.SET_SECRET_LOCK: get_namespace_params(
                type='atomic-swap-set-secret-lock', parser=protos.AtomicSwapSetSecretLockPayload(),
            ),
            protos.AtomicSwapMethod.CLOSE: get_namespace_params(
                type='atomic-swap-close', parser=protos.AtomicSwapClosePayload(),
            ),
        },
        RemmeFamilyName.PUBLIC_KEY.value: {
            protos.PubKeyMethod.STORE: get_namespace_params(
                type='store public key', parser=protos.NewPubKeyPayload(),
            ),
            protos.PubKeyMethod.REVOKE: get_namespace_params(
                type='revoke public key', parser=protos.RevokePubKeyPayload(),
            ),
        },
    }

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

    async def get_blocks(self, query=None):
        """
        Get all blocks from REMChain.
        You can specify one or more query parameters.
        @example
        Without query
        ```python
        blocks = await remme.blockchain_info.get_blocks()
        print(blocks)
        ```

        Start from specifying block number
        ```python
        blocks = await remme.blockchain_info.get_blocks({'start':4})
        print(blocks)
        ```

        Reverse output
        ```python
        blocks = await remme.blockchain_info.get_blocks({'reverse':'false'})
        print(blocks)
        ```

        Specify limit of output
        ```python
        blocks = await remme.blockchain_info.get_blocks({'limit':2})
        print(blocks)
        ```

        Specify head of block for start
        ```python
        blocks = await remme.blockchain_info.get_blocks({
            'head':'9d2dc2ab673d028bc1dd8b5be8d2d885e4383a827cd0261f58334252bf807c08113207eabbd12d0786d6bba5378a791129f9c520c17597b5504d4b547ef57491'
        })
        print(blocks)
        ```
        :param query: dict
        :return block list
        """
        if query:

            if isinstance(query.get('start'), int):

                start = hex(query.get('start')).lstrip('0x')[-16:]
                query['start'] = f'0x{start.zfill(16)}'

            query = BaseQuery(query=query).get()

        return await self._remme_api.send_request(
            method=RemmeMethods.BLOCKS,
            params=query,
        )

    async def get_block_by_id(self, id):
        """
        Get block by id (header_signature) from REMChain.
        Specify limit of output
        @example
        ```python
        block = await remme.blockchain_info.get_block_by_id(
            '9d2dc2ab673d028bc1dd8b5be8d2d885e4383a827cd0261f58334252bf807c08113207eabbd12d0786d6bba5378a791129f9c520c17597b5504d4b547ef57491'
        )
        print(block)
        ```
        :param id: string
        :return block
        """
        self._check_id(id=id)

        return await self._remme_api.send_request(
            method=RemmeMethods.FETCH_BLOCK,
            params={'id': id},
        )

    async def get_block_info(self, query=None):
        """
        Get information about block.
        @example
        Without parameters
        ```python
        block_info = await remme.blockchain_info.get_block_info()
        print(block_info)
        ```

        Start from specifying block number
        ```python
        block_info = await remme.blockchain_info.get_block_info({'start':2})
        print(block_info)
        ```

        Specify limit of output
        ```python
        block_info = await remme.blockchain_info.get_block_info({'limit':2})
        print(block_info)
        ```
        :param query: dict
        :return block info
        """
        blocks = await self._remme_api.send_request(
            method=RemmeMethods.BLOCK_INFO,
            params=query,
        )

        if blocks is None:
            raise Exception('Unknown error occurs in the server.')

        return BlockInfo(data=blocks[0])

    async def get_batches(self, query=None):
        """
        Get all batches from REMChain.
        @example
        Without parameters
        ```python
        batches = await remme.blockchain_info.get_batches()
        print(batches)
        ```

        Start from specifying batch header_signature (batch ID)
        ```python
        batches = await remme.blockchain_info.get_batches({
            'start':'8e4dc2ab673d028bc1dd8b5be8d2d885e4383a827cd0261f58334252bf807c08113207eabbd12d0786d6bba5378a791129f9c520c17597b5504d4b547ef5fe5c'
        })
        print(batches)
        ```

        Reverse output
        ```python
        batches = await remme.blockchain_info.get_batches({'reverse':'false'})
        print(batches)
        ```

        Specify limit of output
        ```python
        batches = await remme.blockchain_info.get_batches({'limit':2})
        print(batches)
        ```

        Specify head of block for start
        ```python
        batches = await remme.blockchain_info.get_batches({
            'head':'9d2dc2ab673d028bc1dd8b5be8d2d885e4383a827cd0261f58334252bf807c08113207eabbd12d0786d6bba5378a791129f9c520c17597b5504d4b547ef57491'
        })
        print(batches)
        ```
        :param query: dict
        :return batch list
        """
        if query:
            query = BaseQuery(query=query).get()

        return await self._remme_api.send_request(
            method=RemmeMethods.BATCHES,
            params=query,
        )

    async def get_batches_by_id(self, id):
        """
        Get batch by id (header_signature) from REMChain.
        @example
        ```python
        batch = await remme.blockchain_info.get_batches_by_id(
            '9d2dc2ab673d028bc1dd8b5be8d2d885e4383a827cd0261f58334252bf807c08113207eabbd12d0786d6bba5378a791129f9c520c17597b5504d4b547ef57491'
        )
        print(batch)
        ```
        :param id: string
        :return batch
        """
        self._check_id(id=id)

        return await self._remme_api.send_request(
            method=RemmeMethods.FETCH_BATCH,
            params={'id': id},
        )

    async def get_batch_status(self, batch_id):
        """
        Get status of batch.
         @example
        ```python
        batch_status = await remme.blockchain_info.get_batch_status(
            '8e4dc2ab673d028bc1dd8b5be8d2d885e4383a827cd0261f58334252bf807c08113207eabbd12d0786d6bba5378a791129f9c520c17597b5504d4b547ef5fe5c'
        )
        print(batch_status)
        ```
        :param batch_id: string
        :return batch status
        """
        self._check_id(id=batch_id)

        return await self._remme_api.send_request(
            method=RemmeMethods.BATCH_STATUS,
            params={'id': batch_id},
        )

    async def get_state(self, query=None):
        """
        Get states in REMChain.
        @example
        Without parameters
        ```python
        states = await remme.blockchain_info.get_state()
        print(states)
        ```

        Start from specifying state address
        ```python
        states = await remme.blockchain_info.get_state({
            'start':'6a437247a1c12c0fb03aa6e242e6ce988d1cdc7fcc8c2a62ab3ab1202325d7d677e84c'
        })
        print(states)
        ```

        Reverse output
        ```python
        states = await remme.blockchain_info.get_state({'reverse':'false'})
        print(states)
        ```

        Specify limit of output
        ```python
        states = await remme.blockchain_info.get_state({'limit':2})
        print(states)
        ```

        Specify head of block for start
        ```python
        states = await remme.blockchain_info.get_state({
            'head':'f650727dad9a402656179904e95144b1ee1dd4b78a696a4d6d6122c82f5b78fe29c07d45d8842e435d2266e58a18c846137d351b840c4d6fed60b1b71edcb3c9'
        })
        print(states)
        ```
        :param query: dict
        :return state list
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
        @example
        ```python
        state = await remme.blockchain_info.get_state_by_address(
            '6a437247a1c12c0fb03aa6e242e6ce988d1cdc7fcc8c2a62ab3ab1202325d7d677e84c'
        )
        print(state)
        ```
        :param address: string
        :return state
        """
        self._check_address(address=address)

        return await self._remme_api.send_request(
            method=RemmeMethods.FETCH_STATE,
            params={'address': address},
        )

    async def parse_state_data(self, state):
        """
        Parse state data.
        @example
        ```python
        state = await remme.blockchain_info.get_state_by_address(
            '6a437247a1c12c0fb03aa6e242e6ce988d1cdc7fcc8c2a62ab3ab1202325d7d677e84c'
        )
        print(state)
        state['address'] = '6a437247a1c12c0fb03aa6e242e6ce988d1cdc7fcc8c2a62ab3ab1202325d7d677e84c'
        parsed_state = await remme.blockchain_info.parse_state_data(state)
        print(parsed_state)
        ```
        :param state: dict
        :return parse state: dict
        """
        address = state.get('address')

        if address is None:
            raise Exception('State should have address for parsing.')

        if not RemmeBlockchainInfo._address.get(address[0:6]):
            raise Exception(f'This address {address} don\'t supported for parsing.')

        namespace_params = RemmeBlockchainInfo._address.get(address[0:6])
        type, parser = namespace_params.get('type'), namespace_params.get('parser')

        parser.ParseFromString(base64.b64decode(state.get('data')))

        return {
            'data': parser,
            'type': type,
        }

    async def get_transactions(self, query=None):
        """
        Get all transactions from REMChain.
        @example
        Without parameters
        ```python
        transactions = await remme.blockchain_info.get_transactions()
        print(transactions)
        ```

        Start from specifying transactions header_signature
        ```python
        transactions = await remme.blockchain_info.get_transactions({
            'start':'f32fc2ab673d028bc1dd8b5be8d2d885e4383a827cd0261f58334252bf807c08113207eabbd12d0786d6bba5378a791129f9c520c17597b5504d4b547ef543fe'
        })
        print(transactions)
        ```

        Reverse output
        ```python
        transactions = await remme.blockchain_info.get_transactions({'reverse':'false'})
        print(transactions)
        ```

        Specify limit of output
        ```python
        transactions = await remme.blockchain_info.get_transactions({'limit':2})
        print(transactions)
        ```

        Specify head of block for start
        ```python
        transactions = await remme.blockchain_info.get_transactions({
            'head':'9d2dc2ab673d028bc1dd8b5be8d2d885e4383a827cd0261f58334252bf807c08113207eabbd12d0786d6bba5378a791129f9c520c17597b5504d4b547ef57491'
        })
        print(transactions)
        ```
        :param query: dict
        :return transactions list
        """
        if query:
            query = BaseQuery(query=query).get()

        return await self._remme_api.send_request(
            method=RemmeMethods.TRANSACTIONS,
            params=query,
        )

    async def get_transaction_by_id(self, id):
        """
        Get transaction by id (header_signature) from REMChain.
        @example
        ```python
        transaction = await remme.blockchain_info.get_transaction_by_id(
            'f32fc2ab673d028bc1dd8b5be8d2d885e4383a827cd0261f58334252bf807c08113207eabbd12d0786d6bba5378a791129f9c520c17597b5504d4b547ef543fe'
        )
        print(transaction)
        ```
        :param id: string
        :return block
        """
        self._check_id(id=id)

        return await self._remme_api.send_request(
            method=RemmeMethods.FETCH_TRANSACTION,
            params={'id': id},
        )

    async def parse_transaction_payload(self, transaction):
        """
        Parse transaction payload. Take transaction and return object with payload and type.
        @example
        ```python
        transaction = await remme.blockchain_info.get_transaction_by_id(
            'f32fc2ab673d028bc1dd8b5be8d2d885e4383a827cd0261f58334252bf807c08113207eabbd12d0786d6bba5378a791129f9c520c17597b5504d4b547ef543fe'
        )
        print(transaction)
        parsed_transaction = remme.blockchain_info.parse_transaction_payload(transaction.get('data'))
        print(parsed_transaction)
        ```
        :param transaction: dict
        """
        family_name = transaction.get('header').get('family_name')

        if family_name not in RemmeBlockchainInfo._correspond:
            raise Exception(f'Family name {family_name} don\'t supported for parsing.')

        payload = base64.b64decode(transaction.get('payload'))

        transaction_payload = protos.TransactionPayload()
        transaction_payload.ParseFromString(payload)

        method = transaction_payload.method
        data = transaction_payload.data

        namespace_params = RemmeBlockchainInfo._correspond.get(family_name).get(method)

        type, parser = namespace_params.get('type'), namespace_params.get('parser')

        parser.ParseFromString(data)

        return {
            'payload': parser,
            'type': type,
        }

    async def get_network_status(self):
        """
        Get network status for node.
        @example
        ```python
        network_status = await remme.blockchain_info.get_network_status()
        print(network_status)
        ```
        :return network status
        """
        network_status_data = await self._remme_api.send_request(method=RemmeMethods.NETWORK_STATUS)

        return NetworkStatus(network_status=network_status_data)

    async def get_peers(self):
        """
        Get peers that connected to this node.
        @example
        ```python
        peers = await remme.blockchain_info.get_peers()
        print(peers)
        ```
        :return list of peers
        """
        return (await self._remme_api.send_request(method=RemmeMethods.PEERS)).get('data')

    # TODO: uncomment after refactoring receipts
    # def get_receipts(self, ids):
    #     """
    #     Get transactions receipts
    #     :param ids: list of string
    #     :return: receipt list
    #     """
    #     for id in ids:
    #         self._check_id(id=id)
    #
    #     return (await self._remme_api.send_request(method=RemmeMethods.RECEIPTS, params={'ids': ids})).get('data')
