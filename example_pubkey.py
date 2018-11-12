from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization

from remme.models.create_certificate_dto import CreateCertificateDto
from remme.remme import Remme
import asyncio
import time
from datetime import datetime, timedelta


async def example():
    private_key_hex = "7f752a99bbaf6755dc861bb4a7bb19acb913948d75f3b718ff4545d01d9d4ff5"
    key_file = open("test_rsa_private.key", "rb")
    remme = Remme(private_key_hex=private_key_hex)
    private_key = serialization.load_pem_private_key(key_file.read(), password=b"53609199", backend=default_backend())
    data = {
        "data": "store data",
        "private_key": private_key,
        "public_key": private_key.public_key(),
        "valid_from": int(datetime.utcnow().strftime("%s")),
        "valid_to": int((datetime.utcnow() + timedelta(days=365)).strftime("%s"))

    }
    pubkey_storage_transaction_result = await remme.public_key_storage.store(**data)
    async for response in pubkey_storage_transaction_result.connect_to_web_socket():
        print("connected")
        await pubkey_storage_transaction_result.close_web_socket()


loop = asyncio.get_event_loop()
loop.run_until_complete(example())
