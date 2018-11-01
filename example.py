from remme.models.base_transaction_response import BaseTransactionResponse
from remme.remme import Remme
from remme.remme_methods import RemmeMethods
from remme.remme_websocket import RemmeWebSocket
import asyncio


async def example():
    private_key_hex = "7f752a99bbaf6755dc861bb4a7bb19acb913948d75f3b718ff4545d01d9d4ff5"
    # _address = "02926476095ea28904c11f22d0da20e999801a267cd3455a00570aa1153086eb13"
    reciver_address = "03823c7a9e285246985089824f3aaa51fb8675d08d84b151833ca5febce37ad61e"

    private_key_hex = "ac124700cc4325cc2a78b22b9acb039d9efe859ef673b871d55d1078391934f9"
    # some_remme_address = "03c75297511ce0cfd1315a045dd0db2a4a1710efed94f0f94ad993b5dfe2e33b62"

    # I want to create tokens for testing
    # I create some account, and generate public key to receive funds.

    remme = Remme(private_key_hex=private_key_hex)
    receiver_public_key_hex = remme._account.public_key_hex
    print(f"generated private key hex for receiving funds {receiver_public_key_hex}")

    # Next I get private key of my Node

    node_key = await remme._api.send_request(RemmeMethods.NODE_PRIVATE_KEY)
    print(f"node key {node_key}")

    # Next I create account with Node private key

    remme = Remme(private_key_hex=node_key)

    # I create transaction signed by Node to send funds to test account

    beforeBalance = await remme.token.get_balance(receiver_public_key_hex)
    print(f'balance is: {beforeBalance} REM')  # >>> balance: 0
    transaction_result = await remme.token.transfer(receiver_public_key_hex, 10)

    ws_connection = await transaction_result.connect_to_web_socket()
    async for msg in ws_connection._socket:
        await ws_connection.close_web_socket()
        print(f"websocket message {msg.data}")

        batch_id = transaction_result._data['batch_id'][0]
        print(f"batch id {batch_id}")
        await asyncio.sleep(10)
        afterBalance = await remme.token.get_balance(receiver_public_key_hex)
        print(f'balance is: {afterBalance} REM')  # >>> balance: 1000

        await asyncio.sleep(10)
        batch_status = await remme.batch.get_status(batch_id)
        print(f"batch status {batch_status}")

    # using web socket as context manager

    # async with BaseTransactionResponse(node_address="localhost:8080", ssl_mode=False, batch_id=batch_id) as ws:
    #     print("connected")
    #     await ws.close_web_socket()


loop = asyncio.get_event_loop()
loop.run_until_complete(example())
