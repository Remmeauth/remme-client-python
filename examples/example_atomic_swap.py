import asyncio
import os
import sys
from aiohttp_json_rpc.exceptions import RpcGenericServerDefinedError

sys.path.insert(0, os.path.realpath('./'))

from remme import Remme
from remme.utils import web3_hash


async def example():

    remme = Remme(account_config={
        'private_key_hex': 'f4f551c178104595ff184f1786ddb2bfdc74b24562611edcab90d4729fb4bab8',
    })

    swap_id = '133102e41346242476b15a3a7966eb5249271025fc7fb0b37ed3fdb4bcce3806'
    secret_key = '3e0b064c97247732a3b345ce7b2a835d928623cb2871c26db4c2539a38e61a16'
    secret_lock = web3_hash(secret_key)
    receiver_address = '112007484def48e1c6b77cf784aeabcac51222e48ae14f3821697f4040247ba01558b1'
    sender_address_non_local = '0xe6ca0e7c974f06471759e9a05d18b538c5ced11e'

    init = await remme.swap.init(
        receiver_address=receiver_address,
        sender_address_non_local=sender_address_non_local,
        amount=10,
        swap_id=swap_id,
        secret_lock_by_solicitor=secret_lock,
    )
    print(f'Init batch id: {init.batch_id}')

    while True:

        try:
            swap_info = await remme.swap.get_info(swap_id=swap_id)
            print(f'Info: {swap_info.data}')

            public_key = await remme.swap.get_public_key()
            print(f'Public key: {public_key}')

            close = await remme.swap.close(swap_id=swap_id, secret_key=secret_key)
            print(f'Close batch id: {close.batch_id}')

            swap_info_after_close = await remme.swap.get_info(swap_id=swap_id)
            print(f'After close info: {swap_info_after_close.data}')

            break

        except RpcGenericServerDefinedError:
            continue


loop = asyncio.get_event_loop()
loop.run_until_complete(example())
