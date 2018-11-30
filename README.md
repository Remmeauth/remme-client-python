<img src="https://avatars1.githubusercontent.com/u/29229038" />

REMME Python Client
===================

**An open source Python integration library for REMChain, simplifying the access and interaction with REMME nodes both public or permissioned.**

## How to use

### 1. Install and run REMME node with required REST API methods enabled

You can check out how to do that at [REMME core repo](<https://github.com/Remmeauth/remme-core/>).

*Note: you can enable/disable methods by modifying `REMME_REST_API_AVAILABLE_METHODS` environment variable at the `.env` file.*

### 2. Install the latest version of library to your Python project

```
pip3 install remme
```

## Examples

#### Remme client

```python
from remme.remme import Remme

private_key_hex = 'bcf42d0194f7f6448e6f03ca0fa1f53cc3fe7768d546cd4d028144aba654d7aa'
network_config = {
    'node_address': 'localhost',
    'node_port': '8080',
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

## License

REMME software and documentation are licensed under `Apache License Version 2.0 <LICENSE>`.
