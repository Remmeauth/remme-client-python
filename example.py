from remme.models.i_public_key_store import IPublicKeyStore
from remme.remme import Remme
import asyncio


async def example():
    private_key_hex = "7f752a99bbaf6755dc861bb4a7bb19acb913948d75f3b718ff4545d01d9d4ff5"
    another_private_key_hex = "ac124700cc4325cc2a78b22b9acb039d9efe859ef673b871d55d1078391934f9"

    remme = Remme(private_key_hex=private_key_hex)
    data = IPublicKeyStore()
    store_result = remme.public_key_storage.store(data)
    async for msg in store_result.connect_to_web_socket():
        print("connected")
        await store_result.close_web_socket()


loop = asyncio.get_event_loop()
loop.run_until_complete(example())
