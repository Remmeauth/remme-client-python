import asyncio
import os
import sys

sys.path.insert(0, os.path.realpath('./'))

from remme import Remme


async def example():
    """
    Generate new account and set it to Remme client.
    """
    account = Remme().generate_account()

    public_key_hex = account.public_key_hex
    print(f'Public key hex: {public_key_hex}')

    data = 'some data'
    signed_data = account.sign(data)
    print(f'Signed data by senders account: {signed_data}')

    is_verify = account.verify(data, signed_data)
    print(f'Is verified by senders account: {is_verify}')  # True

    another_account = Remme().generate_account()
    is_verify_in_another_account = another_account.verify(data, signed_data)
    print(f'Is verified by another account: {is_verify_in_another_account}')  # False


loop = asyncio.get_event_loop()
loop.run_until_complete(example())
