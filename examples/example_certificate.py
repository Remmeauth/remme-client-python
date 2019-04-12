import asyncio
import os
import sys
from aiohttp_json_rpc.exceptions import RpcGenericServerDefinedError
from datetime import datetime

sys.path.insert(0, os.path.realpath('./'))

from remme import Remme


async def example():

    remme = Remme(account_config={
        'private_key_hex': 'f4f551c178104595ff184f1786ddb2bfdc74b24562611edcab90d4729fb4bab8',
    })

    certificate_transaction_result = await remme.certificate.create_and_store(
        common_name='user_name',
        email='user@email.com',
        name='John',
        surname='Smith',
        country_name='US',
        validity=360,
        serial=str(datetime.now())
    )
    certificate = certificate_transaction_result.certificate

    while True:

        try:
            info = await remme.certificate.get_info(certificate)
            print(f'Info: {info.data}')

            certificate_status = await remme.certificate.check(certificate)
            print(f'Certificate is valid: {certificate_status}')
            break

        except RpcGenericServerDefinedError:
            continue


loop = asyncio.get_event_loop()
loop.run_until_complete(example())
