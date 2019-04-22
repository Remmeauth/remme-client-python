import asyncio
import os
import sys

sys.path.insert(0, os.path.realpath('./'))

from remme import Remme
from remme.utils import dict_to_pretty_json


async def example():

    remme = Remme(account_config={
        'private_key_hex': 'f4f551c178104595ff184f1786ddb2bfdc74b24562611edcab90d4729fb4bab8',
    })

    block_info = await remme.blockchain_info.get_block_info({'start': 1})
    print(f'Block info: {dict_to_pretty_json(block_info)}')

    # network = await remme.blockchain_info.get_network_status()
    # print(f'Network status: {dict_to_pretty_json(network.data)}')
    #
    # blocks = await remme.blockchain_info.get_blocks()
    # print(f'Blocks: {dict_to_pretty_json(blocks)}')
    #
    # block = await remme.blockchain_info.get_block_by_id(blocks.get('data')[0].get('header_signature'))
    # print(f'Block: {dict_to_pretty_json(block)}')
    #
    # batches = await remme.blockchain_info.get_batches()
    # print(f'Batches: {dict_to_pretty_json(batches)}')
    #
    # batch = await remme.blockchain_info.get_batch_by_id(batches.get('data')[0].get('header_signature'))
    # print(f'Batch: {dict_to_pretty_json(batch)}')
    #
    # batch_status = await remme.blockchain_info.get_batch_status(batches.get('data')[1].get('header_signature'))
    # print(f'Batch status: {batch_status}')
    #
    # transactions = await remme.blockchain_info.get_transactions()
    # print(f'Transactions: {dict_to_pretty_json(transactions)}')
    #
    # transaction = await remme.blockchain_info.get_transaction_by_id(
    #     transactions.get('data')[-3].get('header_signature'),
    # )
    # print(f'Transaction: {dict_to_pretty_json(transaction)}')
    #
    # payload = await remme.blockchain_info.parse_transaction_payload(transaction.get('data'))
    # print(f'Transaction payload: {payload}')
    #
    # states = await remme.blockchain_info.get_states()
    # print(f'States: {dict_to_pretty_json(states)}')
    #
    # state = await remme.blockchain_info.get_state_by_address(states.get('data')[-1].get('address'))
    # print(f'State: {dict_to_pretty_json(state)}')
    #
    # state['address'] = '112007be95c8bb240396446ec359d0d7f04d257b72aeb4ab1ecfe50cf36e400a96ab9c'
    #
    # data = await remme.blockchain_info.parse_state_data(state)
    # print(f'Parse data: {data}')
    #
    # peers = await remme.blockchain_info.get_peers()
    # print(f'Peers: {peers}')
    #
    # receipts = await remme.blockchain_info.get_receipts([transactions.get('data')[1].get('header_signature')])
    # print(f'Receipts: {dict_to_pretty_json(receipts)}')


loop = asyncio.get_event_loop()
loop.run_until_complete(example())
