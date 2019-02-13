import asyncio

from remme.models.websocket.base_transaction_response import BaseTransactionResponse


async def example():

    batch_id = "bc1b32a5ead06cc9203d0019a54391b40a7eadb61c80675de60ecc83d4be6fed" \
               "0c795dfbccc717e3d52bf3fec8a3cbfc7cf6ab8fc1cdfd07f8b76bf457288060"

    kwargs = {"node_address": "localhost:8080", "ssl_mode": False, "batch_id": batch_id}

    tx = BaseTransactionResponse(**kwargs)

    async for msg in tx.connect_to_web_socket():
        print("connected")
        print("handle some messages")

        await tx.close_web_socket()

    print("connection closed")


loop = asyncio.get_event_loop()
loop.run_until_complete(example())
