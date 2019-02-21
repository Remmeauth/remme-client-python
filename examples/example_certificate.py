import asyncio
from datetime import datetime

from remme import Remme


async def example():

    remme = Remme(private_key_hex='f4f551c178104595ff184f1786ddb2bfdc74b24562611edcab90d4729fb4bab8')

    certificate_transaction_result = await remme.certificate.create_and_store(
        common_name='user_name',
        email='user@email.com',
        name='John',
        surname='Smith',
        country_name='US',
        validity=360,
        serial=str(datetime.now())
    )

    async for response in certificate_transaction_result.connect_to_web_socket():
        print('connected')
        print('certificate', response)
        print(f'Certificate was saved on REMchain at block number: {response.block_number}')
        certificate_status = remme.certificate.check(certificate_transaction_result.certificate)
        print(f'Certificate is_valid = {certificate_status}')
        await certificate_transaction_result.close_web_socket()


loop = asyncio.get_event_loop()
loop.run_until_complete(example())
