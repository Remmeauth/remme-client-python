from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

from remme.remme import Remme
import asyncio
from datetime import datetime, timedelta


async def example():
    private_key_hex = "7f752a99bbaf6755dc861bb4a7bb19acb913948d75f3b718ff4545d01d9d4ff5"
    remme = Remme(private_key_hex=private_key_hex)
    # private_key_file = open("test_rsa_private.key", "rb")
    # public_key_file = open("test_rsa_public.key", "rb")
    # data = {
    #     "data": "store data",
    #     "private_key": private_key_file.read(),
    #     "public_key": public_key_file.read(),
    #     "valid_from": int(datetime.utcnow().strftime("%s")),
    #     "valid_to": int((datetime.utcnow() + timedelta(days=365)).strftime("%s"))
    # }
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048, backend=default_backend())
    data = {
        "data": "store data",
        "private_key": private_key,
        "public_key": private_key.public_key(),
        "valid_from": int(datetime.utcnow().strftime("%s")),
        "valid_to": int((datetime.utcnow() + timedelta(days=365)).strftime("%s"))
    }
    pubkey_storage_transaction_result = await remme.public_key_storage.store(**data)

    batch_status = await remme.batch.get_status(pubkey_storage_transaction_result.batch_id)
    print(f"batch status {batch_status}\n")

    async for response in pubkey_storage_transaction_result.connect_to_web_socket():
        print("connected")
        batch_status = await remme.batch.get_status(pubkey_storage_transaction_result.batch_id)
        print(f"batch status {batch_status}\n")
        # if response.status == BatchStatus.COMMITTED.value:
        #     batch_status = await remme.batch.get_status(pubkey_storage_transaction_result.batch_id)
        #     print(f"batch status {batch_status}\n")
        await pubkey_storage_transaction_result.close_web_socket()


loop = asyncio.get_event_loop()
loop.run_until_complete(example())
