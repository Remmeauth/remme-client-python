import asyncio
from remme import Remme
from remme.models.general.batch_status import BatchStatus


async def example():

    remme = Remme(private_key_hex='f4f551c178104595ff184f1786ddb2bfdc74b24562611edcab90d4729fb4bab8')

    some_remme_address = '1120077f88b0b798347b3f52751bb99fa8cabaf926c5a1dad2d975d7b966a85b3a9c21'

    balance = await remme.token.get_balance(some_remme_address)
    print(f'Account {some_remme_address}, balance - {balance} REM')

    transaction_result = await remme.token.transfer(some_remme_address, 10)
    print(f'Sending tokens...BatchId: {transaction_result.batch_id}')

    async for batch_info in transaction_result.connect_to_web_socket():
        if batch_info.status == BatchStatus.COMMITTED.value:
            new_balance = await remme.token.get_balance(some_remme_address)
            print(f'Account {some_remme_address}, balance - {new_balance} REM')
            await transaction_result.close_web_socket()


loop = asyncio.get_event_loop()
loop.run_until_complete(example())
