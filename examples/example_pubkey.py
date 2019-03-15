import asyncio
import os
import sys
from datetime import datetime, timedelta

sys.path.insert(0, os.path.realpath('./'))

from remme import Remme
from remme.models.keys.key_type import KeyType
from remme.models.keys.rsa_signature_padding import RsaSignaturePadding


async def example():

    remme = Remme(private_key_hex='f4f551c178104595ff184f1786ddb2bfdc74b24562611edcab90d4729fb4bab8')

    keys = remme.keys.construct(KeyType.RSA)

    current_timestamp = int(datetime.now().timestamp())
    current_timestamp_plus_year = int(current_timestamp + timedelta(365).total_seconds())

    pubkey_transaction_result = await remme.public_key_storage.create_and_store(
        data='some',
        keys=keys,
        rsa_signature_padding=RsaSignaturePadding.PSS,
        valid_from=current_timestamp,
        valid_to=current_timestamp_plus_year,
        do_owner_pay=False,
    )

    async for response in pubkey_transaction_result.connect_to_web_socket():
        print('connected')
        print(response)
        info = await remme.public_key_storage.get_info(keys.address)
        print('info', info)
        is_valid = await remme.public_key_storage.check(keys.address)
        print('is_valid:', is_valid)
        public_key_addresses = await remme.public_key_storage.get_account_public_keys(remme.account.address)
        print('list_public_key_addresses:', public_key_addresses)
        await pubkey_transaction_result.close_web_socket()


loop = asyncio.get_event_loop()
loop.run_until_complete(example())
