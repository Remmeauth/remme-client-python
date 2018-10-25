from remme.remme import Remme
import asyncio


async def example():
    private_key_hex = "7f752a99bbaf6755dc861bb4a7bb19acb913948d75f3b718ff4545d01d9d4ff5"
    _address = "02926476095ea28904c11f22d0da20e999801a267cd3455a00570aa1153086eb13"
    # _address = "03823c7a9e285246985089824f3aaa51fb8675d08d84b151833ca5febce37ad61e"

    # private_key_hex = "ac124700cc4325cc2a78b22b9acb039d9efe859ef673b871d55d1078391934f9"
    # some_remme_address = "03c75297511ce0cfd1315a045dd0db2a4a1710efed94f0f94ad993b5dfe2e33b62"

    remme = Remme(private_key_hex=private_key_hex)

    query = {"start": 0}
    blocks = await remme.blockchain_info.get_blocks(query)
    print(f"blocks {blocks}")

    node_key = await remme._rest.send_rpc_request(remme._rest.methods.NODE_PRIVATE_KEY.value[0])
    print(f"node key {node_key}")

    atomic_swap_public_key = await remme.swap.get_public_key()
    print(f"atomic swap public key {atomic_swap_public_key}")

    node_info = await remme.blockchain_info.get_network_status()
    print(f"node info {node_info}")

    # block_number = await remme._rest.get_block_number()
    # print(f"block number {block_number}")

    # token

    beforeBalance = await remme.token.get_balance(_address)
    print(f'balance is: {beforeBalance} REM')  # >>> balance: 0
    await remme.token.transfer(_address, 1000)
    await asyncio.sleep(10)
    afterBalance = await remme.token.get_balance(_address)
    print(f'balance is: {afterBalance} REM')  # >>> balance: 1000

    # certificate

    # certificate_data = {
    #     'commonName': "some_user_name",
    #     'email': "grzegorz_brzęczyszczykiewicz@mail.pl",
    #     'name': "Grzegorz",
    #     'surname': "Brzęczyszczykiewicz",
    #     'contryName': "Rzeczpospolita Polska",
    #     'validity': 360,
    #     'serial': 'some serial'
    # }
    # result = await remme.certificate.create_and_store(certificate_data)
    # print(f'certificate transaction result: {result}')
    # print(f'certificate stored in block: {result.block_number}')
    # status = await remme.certificate.check(result.certificate)
    # print(f'certificate is valid: {status.valid}')


loop = asyncio.get_event_loop()
loop.run_until_complete(example())
