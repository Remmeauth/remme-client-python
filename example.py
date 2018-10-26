from remme.remme import Remme
import asyncio


async def example():
    private_key_hex = "7f752a99bbaf6755dc861bb4a7bb19acb913948d75f3b718ff4545d01d9d4ff5"
    # _address = "02926476095ea28904c11f22d0da20e999801a267cd3455a00570aa1153086eb13"
    reciver_address = "03823c7a9e285246985089824f3aaa51fb8675d08d84b151833ca5febce37ad61e"

    private_key_hex = "ac124700cc4325cc2a78b22b9acb039d9efe859ef673b871d55d1078391934f9"
    # some_remme_address = "03c75297511ce0cfd1315a045dd0db2a4a1710efed94f0f94ad993b5dfe2e33b62"

    remme = Remme(private_key_hex=private_key_hex)
    generated_private_key_hex = remme._account.get_public_key_hex()
    sender_address = remme._account.address
    print(f"generated private key hex {generated_private_key_hex}")
    print(f"sender address {sender_address}")

    node_key = await remme._rest.send_rpc_request(remme._rest.methods.NODE_PRIVATE_KEY)
    print(f"node key {node_key}")

    query = {"start": 0}
    blocks = await remme.blockchain_info.get_blocks(query)
    print(f"blocks {blocks}")

    atomic_swap_public_key = await remme.swap.get_public_key()
    print(f"atomic swap public key {atomic_swap_public_key}")

    node_info = await remme.blockchain_info.get_network_status()
    print(f"node info {node_info}")

    block_number = await remme._rest.get_block_number()
    print(f"block number {block_number}")

    # account

    remme = Remme()
    tx = await remme.token._create_transfer_tx(reciver_address, 10)
    print(f"tx {tx.header}")
    signature = remme._account.sign(tx.header)
    print(f"signature {signature}")
    is_valid = remme._account.verify(signature, tx.header)
    print(f"tx is valid ? - {is_valid}")

    # token

    beforeBalance = await remme.token.get_balance(reciver_address)
    print(f'balance is: {beforeBalance} REM')  # >>> balance: 0
    batch_id = await remme.token.transfer(reciver_address, 1000)
    print(f"batch id {batch_id}")
    await asyncio.sleep(10)
    afterBalance = await remme.token.get_balance(reciver_address)
    print(f'balance is: {afterBalance} REM')  # >>> balance: 1000

    await asyncio.sleep(10)
    batch_status = await remme.batch.get_status(batch_id)
    print(f"batch status {batch_status}")

    batch = await remme.blockchain_info.get_batch_by_id(batch_id)
    print(f"batch {batch}")


loop = asyncio.get_event_loop()
loop.run_until_complete(example())
