import asyncio


class RemmeToken:

    rest = None
    transaction_service = None

    def __init__(self, rest, transaction_service):
        self.rest = rest
        self.transaction_service = transaction_service

    def validate_transfer_data(self, public_key_to, amount):
        if amount <= 0:
            raise Exception("Invalid amount")
        return self.validate_public_key(public_key_to), amount

    async def transfer(self, public_key_to, amount):
        raise NotImplementedError

    def validate_public_key(self, key):
        if len(key) != 66:
            raise Exception("Invalid key")
        return key

    async def get_balance(self, public_key):
        return await self.rest.get_balance(public_key=self.validate_public_key(public_key))
