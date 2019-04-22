
![Remme icon](https://habrastorage.org/webt/l8/37/ql/l837ql83zzeeoxikv58v5av5jsi.png)

# Remme Python Client

[![Release](https://img.shields.io/github/release/Remmeauth/remme-client-python.svg)](https://github.com/Remmeauth/remme-client-python/releases)
[![PyPI version shields.io](https://img.shields.io/pypi/v/remme.svg)](https://pypi.python.org/pypi/remme/)
[![PyPI Downloads](https://img.shields.io/pypi/dm/remme.svg)](https://pypi.python.org/pypi/remme)
[![Documentation status](https://readthedocs.org/projects/remme/badge/?version=latest)](http://remme.readthedocs.io/?badge=latest)
[![PyPI license](https://img.shields.io/pypi/l/remme.svg)](https://pypi.python.org/pypi/remme/)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/remme.svg)](https://pypi.python.org/pypi/remme/)

An open source Python integration library for REMChain, simplifying the access
and interaction with Remme nodes both public or permissioned.

* [How to use](#how-to-use)
    * [1. Install Remme protocol](#1-install-remme-protocol)
    * [2. Install dependencies](#2-install-dependencies)
    * [3. Install library](#3-install-library)
* [Examples](#examples)
    * [Remme client](#remme-client)
    * [Tokens](#tokens)
    * [Certificates](#certificates)
    * [Subscribing to Events](#subscribing-to-events)
* [Contributing](#contributing)
* [License](#license)

## How to use

### 1. Install Remme protocol

Install and run Remme protocol with required RPC API methods enabled.

You can check out how to do that at [Remme core repo](<https://github.com/Remmeauth/remme-core/>).

### 2. Install dependencies:

Before installing the library, make sure that all the dependencies listed are installed.

**Required by one of the requirements [system packages list](https://github.com/ludbb/secp256k1-py#installation-with-compilation)**

```bash
$ sudo apt-get update
$ sudo apt-get install python3-dev python3-setuptools -y
$ sudo apt-get install build-essential automake libtool pkg-config libffi-dev -y
```

### 3. Install library

Install the latest version of library to your Python project from terminal using `pip`:

```bash
$ pip3 install remme
```

## Examples

#### Remme client

```python
from remme import Remme
from remme.models.account.account_type import AccountType

account_config = {
    'private_key_hex': 'f4f551c178104595ff184f1786ddb2bfdc74b24562611edcab90d4729fb4bab8', 
    'account_type': AccountType.USER,
}
network_config = {
    'node_address': 'localhost:8080', 
    'ssl_mode': False,
}

remme = Remme(account_config=account_config, network_config=network_config)
```

#### Tokens

```python
remme_address = '1120077f88b0b798347b3f52751bb99fa8cabaf926c5a1dad2d975d7b966a85b3a9c21'

balance = await remme.token.get_balance(address=remme_address)
print(f'Account — {remme_address}, balance — {balance} REM.')

transaction_result = await remme.token.transfer(address_to=remme_address, amount=10)
print(f'Transaction batch id: {transaction_result.batch_id}')

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
```

#### Subscribing to Events

RemmeEvents is enums which describe all available events.

```python
from remme.models.websocket.events import RemmeEvents

events = await remme.events.subscribe(events=RemmeEvents.AtomicSwap.value)

async for response in events:

    print("connected")
    
    if isinstance(response, dict):
        print(response)
    
    else:
        print(f'State: {response.state}')
        print(f'Sender address: {response.sender_address}')
        print(f'Receiver address: {response.receiver_address}')
        print(f'Amount: {response.amount}')

```

Also we give a possibility to start listen events from previous block by providing last known block id.

```python
from remme.models.websocket.events import RemmeEvents

events = await remme.events.subscribe(
    events=RemmeEvents.AtomicSwap.value, 
    last_known_block_id='db19f0e3b3f001670bebc814e238df48cef059f3f0668f57702ba9ff0c4b8ec45c7298f08b4c2fa67602da27a84b3df5dc78ce0f7774b3d3ae094caeeb9cbc82',
)

async for response in events:

    print("connected")
    
    if isinstance(response, dict):
        print(response)
    
    else:
        print(f'State: {response.state}')
        print(f'Sender address: {response.sender_address}')
        print(f'Receiver address: {response.receiver_address}')
        print(f'Amount: {response.amount}')
```

Unsubscribe from listening events.

```python
await remme.events.unsubscribe(events=RemmeEvents.AtomicSwap.value)
```

## Contributing

Clone the project and install requirements:

```bash
$ git clone git@github.com:Remmeauth/remme-client-python.git && cd remme-client-python
$ pip3 install -r requirements.txt
$ pip3 install -r requirements-dev.txt
```

If you prefer working with the [Docker](https://www.docker.com), follow:

```bash
$ git clone git@github.com:Remmeauth/remme-client-python.git && cd remme-client-python
$ docker build -t remme-client-python . -f Dockerfile
$ docker run -v $PWD:/remme-client-python --name remme-client-python remme-client-python
```

Enter the container bash, check `Python` version and run tests:

```bash
$ docker exec -it remme-client-python bash
$ root@98247c92404d:/remme-client-python# python --version
$ root@98247c92404d:/remme-client-python# pytest -vv tests
```

Clean container and images with the following command:

```bash
$ docker rm $(docker ps -a -q) -f
$ docker rmi $(docker images -q) -f
```

## License

Remme software and documentation are licensed under `Apache License Version 2.0 <LICENSE>`.
