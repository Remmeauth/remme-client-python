import asyncio
import os
import sys
from datetime import datetime, timedelta
from aiohttp_json_rpc.exceptions import RpcGenericServerDefinedError

sys.path.insert(0, os.path.realpath('./'))

from remme import Remme
from remme.models.keys.key_type import KeyType
from remme.models.keys.rsa_signature_padding import RsaSignaturePadding


async def example():

    remme = Remme(account_config={
        'private_key_hex': 'f4f551c178104595ff184f1786ddb2bfdc74b24562611edcab90d4729fb4bab8',
    })

    generate_keys = remme.keys.generate_key_pair(KeyType.RSA)
    print(f'Keys: {generate_keys}')

    construct_keys = remme.keys.construct(KeyType.RSA)
    print(f'Keys: {construct_keys}')

    data = 'sign data'
    signature = construct_keys.sign(data=data)
    print(f'Signature: {signature}')
    is_verify = construct_keys.verify(data=data, signature=signature)
    print(f'Is verify: {is_verify}')

    current_timestamp = int(datetime.now().timestamp())
    current_timestamp_plus_year = int(current_timestamp + timedelta(365).total_seconds())

    pub_key = await remme.public_key_storage.create_and_store(
        data=data,
        keys=construct_keys,
        rsa_signature_padding=RsaSignaturePadding.PSS,
        valid_from=current_timestamp,
        valid_to=current_timestamp_plus_year,
        do_owner_pay=False,
    )

    while True:

        try:
            info = await remme.public_key_storage.get_info(construct_keys.address)
            print('Info:', info.data)
            is_valid = await remme.public_key_storage.check(construct_keys.address)
            print('Public key is valid:', is_valid)
            public_key_addresses = await remme.public_key_storage.get_account_public_keys(remme.account.address)
            print('List public key addresses:', public_key_addresses)
            break

        except RpcGenericServerDefinedError:
            continue


loop = asyncio.get_event_loop()
loop.run_until_complete(example())
