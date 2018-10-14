import asyncio

from remme.remme import Remme

__author__ = 'dethline'


async def hello_remme():
    remme = Remme()
    beforeBalance = remme.token.get_balance("02926476095ea28904c11f22d0da20e999801a267cd3455a00570aa1153086eb13")
    print(f'balance: {beforeBalance}')  # >>> balance: 0
    remme.token.transfer("02926476095ea28904c11f22d0da20e999801a267cd3455a00570aa1153086eb13", 1000)
    await asyncio.sleep(5)
    afterBalance = remme.token.get_balance("02926476095ea28904c11f22d0da20e999801a267cd3455a00570aa1153086eb13")
    print(f'balance: {afterBalance}')  # >>> balance: 1000

loop = asyncio.get_event_loop()
loop.run_until_complete(hello_remme())
loop.close()
