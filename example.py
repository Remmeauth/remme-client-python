from remme.remme import Remme
import asyncio


# private_hex_key = "7f752a99bbaf6755dc861bb4a7bb19acb913948d75f3b718ff4545d01d9d4ff5"
private_hex_key = "ac124700cc4325cc2a78b22b9acb039d9efe859ef673b871d55d1078391934f9"
network_config = {

}

# some_remme_address = "03c75297511ce0cfd1315a045dd0db2a4a1710efed94f0f94ad993b5dfe2e33b62"
some_remme_address = "02926476095ea28904c11f22d0da20e999801a267cd3455a00570aa1153086eb13"


async def transfer_to_address(_address):
    remme = Remme()
    beforeBalance = remme.token.get_balance(_address)
    print(f'balance: {beforeBalance}')  # >>> balance: 0
    remme.token.transfer(_address, 1000)
    await asyncio.sleep(10)
    afterBalance = remme.token.get_balance(_address)
    print(f'balance: {afterBalance}')  # >>> balance: 1000

loop = asyncio.get_event_loop()
loop.run_until_complete(transfer_to_address(some_remme_address))
loop.close()
