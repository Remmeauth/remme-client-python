from remme.models.base_transaction_response import BaseTransactionResponse
from remme.remme import Remme
from remme.remme_methods import RemmeMethods
from remme.remme_websocket import RemmeWebSocket
import asyncio
import json


async def example():
    receiver_private_key_hex = "7f752a99bbaf6755dc861bb4a7bb19acb913948d75f3b718ff4545d01d9d4ff5"
    # _address = "02926476095ea28904c11f22d0da20e999801a267cd3455a00570aa1153086eb13"
    # reciver_address = "03823c7a9e285246985089824f3aaa51fb8675d08d84b151833ca5febce37ad61e"

    sender_private_key_hex = "ac124700cc4325cc2a78b22b9acb039d9efe859ef673b871d55d1078391934f9"
    # some_remme_address = "03c75297511ce0cfd1315a045dd0db2a4a1710efed94f0f94ad993b5dfe2e33b62"

    # start remme; some account without funds
    remme_receiver = Remme(private_key_hex=receiver_private_key_hex)
    receiver_public_key_hex = remme_receiver.account.public_key_hex
    print(f"generated private key hex for receiving funds {receiver_public_key_hex}")

    # start another remme; some account with funds
    remme_sender = Remme(private_key_hex=sender_private_key_hex)

    # check balance before transaction
    beforeBalance = await remme_receiver.token.get_balance(receiver_public_key_hex)
    print(f'balance is : {beforeBalance} REM')
    transaction_result = await remme_sender.token.transfer(receiver_public_key_hex, 10)
    print(f'sending tokens... batch id : {transaction_result.batch_id}')

    ws_connection = await transaction_result.connect_to_web_socket()
    async for msg in ws_connection.socket:
        print(f"websocket message {msg.data}")
        response = json.loads(msg.data)
        if response['status'] == "COMMITTED":
            afterBalance = await remme_sender.token.get_balance(receiver_public_key_hex)
            print(f'balance is: {afterBalance} REM')

    # await asyncio.sleep(10)
    # batch_status = await remme_sender.batch.get_status(batch_id)
    # print(f"batch status {batch_status}")


loop = asyncio.get_event_loop()
loop.run_until_complete(example())
