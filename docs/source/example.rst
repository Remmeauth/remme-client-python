
Examples
========

Examples of using library

Remme client
------------

.. code-block:: python

    from remme.remme import Remme

    private_key_hex = 'bcf42d0194f7f6448e6f03ca0fa1f53cc3fe7768d546cd4d028144aba654d7aa'
    network_config = {
        'node_address': 'localhost:8080',
        'ssl_mode': False,
    }

    remme = Remme(private_key_hex=private_key_hex, network_config=network_config)

Tokens
------

.. code-block:: python

    some_remme_address = '1120077f88b0b798347b3f52751bb99fa8cabaf926c5a1dad2d975d7b966a85b3a9c21'

    balance = await remme.token.get_balance(some_remme_address)
    print(f'Account {some_remme_address}, balance - {balance} REM')

    transaction_result = await remme.token.transfer(some_remme_address, 10)
    print(f'Sending tokens...BatchId: {transaction_result.batch_id}')

    async for batch_info in transaction_result.connect_to_web_socket():
        if batch_info.status == BatchStatus.COMMITTED.value:
            new_balance = await remme.token.get_balance(some_remme_address)
            print(f'Account {some_remme_address}, balance - {new_balance} REM')
            await transaction_result.close_web_socket()

Certificates
------------

.. code-block:: python

    certificate_transaction_result = await remme.certificate.create_and_store(
        common_name='user_name',
        email='user@email.com',
        name='John',
        surname='Smith',
        country_name='US',
        validity=360,
        serial='some serial'
    )

    async for response in certificate_transaction_result.connect_to_web_socket():
        print('certificate', response)
        print(f'Certificate was saved on REMchain at block number: {response.block_number}')
        certificate_status = remme.certificate.check(certificate_transaction_result.certificate)
        print(f'Certificate is_valid = {certificate_status.valid}')
        await certificate_transaction_result.close_web_socket()

Subscribing to Events
---------------------

RemmeEvents is enums which describe all available events.

.. code-block:: python

    from remme.models.websocket.events import RemmeEvents

    events = await remme.events.subscribe(events=RemmeEvents.AtomicSwap.value)
    async for response in events:
        print('connected')
        print('events', response)

Also we give a possibility to start listen events from previous block by providing last known block id.

.. code-block:: python

    from remme.models.websocket.events import RemmeEvents

    events = await remme.events.subscribe(
        events=RemmeEvents.AtomicSwap.value,
        last_known_block_id='db19f0e3b3f001670bebc814e238df48cef059f3f0668f57702ba9ff0c4b8ec45c7298f08b4c2fa67602da27a84b3df5dc78ce0f7774b3d3ae094caeeb9cbc82',
    )
    async for response in events:
        print('connected')
        print('events', response)

**Unsubscribe** from listening events.

.. code-block:: python

    remme.events.unsubscribe()

