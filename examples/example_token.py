import asyncio
import os
import sys

sys.path.insert(0, os.path.realpath('./'))

from remme import Remme
from remme.models.websocket.events import RemmeEvents


async def example():

    remme = Remme(account_config={
        'private_key_hex': 'f4f551c178104595ff184f1786ddb2bfdc74b24562611edcab90d4729fb4bab8',
    })

    address = '112007db8a00c010402e2e3a7d03491323e761e0ea612481c518605648ceeb5ed454f7'

    # subscribe
    events = await remme.events.subscribe(event_type=RemmeEvents.Transfer.value, address=address)

    count = 0
    async for msg in events:

        print("connected")
        print("handle some messages")

        if isinstance(msg, dict):
            print(msg)

        else:
            print('Transfer from:', msg.transfer_from)
            print('Transfer to:', msg.transfer_to)

        balance = await remme.token.get_balance(address=address)
        print(f'Account — {address}, balance — {balance} REM.')

        transaction_result = await remme.token.transfer(address_to=address, amount=10)
        print(f'Transaction batch id: {transaction_result.batch_id}')

        count += 1
        if count == 2:
            # unsubscribe
            await remme.events.unsubscribe(event_type=RemmeEvents.Transfer.value)
            print("connection closed")


loop = asyncio.get_event_loop()
loop.run_until_complete(example())
