import asyncio
import os
import sys

sys.path.insert(0, os.path.realpath('./'))

from remme import Remme


async def example():

    remme = Remme(private_key_hex='f4f551c178104595ff184f1786ddb2bfdc74b24562611edcab90d4729fb4bab8')

    block_info = await remme.blockchain_info.get_block_info()
    print(f'Block info: {block_info}')

    # network = await remme.blockchain_info.get_network_status()
    # print(f'Network status: {network}')

    # blocks = await remme.blockchain_info.get_blocks()
    # print(f'Blocks: {blocks}')

    # block = await remme.blockchain_info.get_block_by_id(blocks.get('data')[1].get('header_signature'))
    # print(f'Block: {block}')

    # batches = await remme.blockchain_info.get_batches()
    # print(f'Batches: {batches}')
    #
    # batch = await remme.blockchain_info.get_batches_by_id(batches.get('data')[1].get('header_signature'))
    # print(f'Batch: {batch}')
    #
    # transactions = await remme.blockchain_info.get_transactions()
    # print(f'Transactions: {transactions}')
    #
    # transaction = await remme.blockchain_info.get_batches_by_id(transactions.get('data')[1].get('header_signature'))
    # print(f'Transaction: {transaction}')
    #
    # payload = await remme.blockchain_info.parse_transaction_payload(transaction.data)
    # print(f'Transaction payload: {payload}')
    #
    # states = await remme.blockchain_info.get_state()
    # print(f'States: {states}')
    #
    # state = await remme.blockchain_info.get_state_by_address(
    #     states.get('data')[len(states.get('data')) - 1].get('address'),
    # )
    # print(f'State: {state}')
    #
    # state['address'] = '6a437247a1c12c0fb03aa6e242e6ce988d1cdc7fcc8c2a62ab3ab1202325d7d677e84c'
    #
    # data = await remme.blockchain_info.parse_state_data(state)
    # print(f'Parse data: {data}')
    #
    # batch_status = await remme.blockchain_info.get_batch_status(batches.get('data')[1].get('header_signature'))
    # print(f'Batch status: {batch_status}')
    #
    # peers = await remme.blockchain_info.get_peers()
    # print(f'Peers: {peers}')
    #
    # receipts = await remme.blockchain_info.get_receipts([
    #     transactions.get('data')[1].get('header_signature'),
    #     '9d2dc2ab673d028bc1dd8b5be8d2d885e4383a827cd0261f58334252bf807c08'
    #     '113207eabbd12d0786d6bba5378a791129f9c520c17597b5504d4b547ef57491'
    # ])
    # print(f'Receipts: {receipts}')


loop = asyncio.get_event_loop()
loop.run_until_complete(example())
