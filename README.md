 <img src="https://avatars1.githubusercontent.com/u/29229038" />

Remme Python Client
===================

**An open source Python integration library for REMChain, simplifying 
the access and interaction with Remme nodes both public or permissioned.**

## How to use

### 1. Install and run Remme protocol with required RPC API methods enabled

You can check out how to do that at [Remme core repo](<https://github.com/Remmeauth/remme-core/>).

### 2. Before installing the library, make sure that all the dependencies listed are installed:
    
**Python3.6**

```
$ sudo add-apt-repository ppa:deadsnakes/ppa
$ sudo apt-get update
$ sudo apt-get install python3.6-dev
$ python3.6 -V or python3.6 --version
```

**Pip**

```
$ sudo apt-get -y install python3-pip
$ pip3 --version or pip3 -V
```

**Some dependency**

```
$ sudo apt-get install build-essential automake libtool pkg-config libffi-dev -y
$ sudo apt-get update && apt-get install pkg-config
```

### 3. Install the latest version of library to your Python project from terminal using `pip`

```
$ pip3 install remme
```

## Examples

#### Remme client

```python
from remme import Remme

private_key_hex = 'bcf42d0194f7f6448e6f03ca0fa1f53cc3fe7768d546cd4d028144aba654d7aa'
network_config = {
    'node_address': 'localhost:8080',
    'ssl_mode': False,
}

remme = Remme(private_key_hex=private_key_hex, network_config=network_config)
```

#### Tokens

```python
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
```

#### Certificates

```python
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
    print(f'Certificate is_valid = {certificate_status}')
    await certificate_transaction_result.close_web_socket()
```

#### Subscribing to Events

RemmeEvents is enums which describe all available events.

```python
from remme.models.websocket.events import RemmeEvents

events = await remme.events.subscribe(events=RemmeEvents.AtomicSwap.value)
async for response in events:
    print('connected')
    print('events', response)
```

Also we give a possibility to start listen events from previous block by providing last known block id.

```python
from remme.models.websocket.events import RemmeEvents

events = await remme.events.subscribe(
    events=RemmeEvents.AtomicSwap.value, 
    last_known_block_id='db19f0e3b3f001670bebc814e238df48cef059f3f0668f57702ba9ff0c4b8ec45c7298f08b4c2fa67602da27a84b3df5dc78ce0f7774b3d3ae094caeeb9cbc82',
)
async for response in events:
    print('connected')
    print('events', response)
```

Unsubscribe from listening events.

```python
remme.events.unsubscribe()
```

## License

Remme software and documentation are licensed under `Apache License Version 2.0 <LICENSE>`.
