import asyncio

from remme.remme import Remme


async def example():
    """
    Generate new account and set it to Remme client.
    """
    sender_private_key_hex = "ac124700cc4325cc2a78b22b9acb039d9efe859ef673b871d55d1078391934f9"

    remme = Remme(private_key_hex=sender_private_key_hex)

    public_key_hex = remme.account.public_key_hex
    print(f'Public key hex: {public_key_hex}')

    data = 'some data'
    signed_data = remme.account.sign(data)
    print(f'Signed data by senders account: {signed_data}')

    is_verify = remme.account.verify(signed_data, data)
    print(f'Is verified by senders account: {is_verify}')  # True

    another_remme = Remme()
    is_verify_in_another_account = another_remme.account.verify(data, signed_data)
    print(f'Is verified by another account: {is_verify_in_another_account}')  # False


loop = asyncio.get_event_loop()
loop.run_until_complete(example())
