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

    def transfer(self, public_key_to, amount):
        valid_public_key_to, valid_amount = self.validate_transfer_data(public_key_to, amount)
        url = "/api/v1/token"
        data = {'pub_key_to': valid_public_key_to, 'amount': valid_amount}
        result = self.rest.post(url=url, data=data)
        if result['status'] == "OK":
            return result['data']
        raise Exception("Failed to create transfer")

    def validate_public_key(self, key):
        if len(key) != 66:
            raise Exception("Invalid key")
        return key

    async def get_balance(self, public_key):
        valid_public_key = self.validate_public_key(public_key)
        url = f'/api/v1/token/{valid_public_key}'
        print(self.rest)
        result = await self.rest.get(url)
        if result['status'] == "OK":
            data = result['data']
            return data['balance']
        raise Exception("Failed to get balance")
