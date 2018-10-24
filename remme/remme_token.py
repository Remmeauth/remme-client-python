from remme.remme_utils import generate_address


class RemmeToken:

    rest = None
    transaction_service = None
    _family_name = "account"
    _family_version = "0.1"

    def __init__(self, rest, transaction_service):
        self.rest = rest
        self.transaction_service = transaction_service

    def validate_amount(self, amount):
        if amount <= 0:
            raise Exception("Invalid amount")
        return amount

    async def transfer(self, public_key_to, amount):
        public_key_to = self.validate_public_key(public_key_to)
        amount = self.validate_amount(amount)
        receiver_address = generate_address(self._family_name, public_key_to)
        print(f"receiver address: {receiver_address}")
        raise NotImplementedError

    def validate_public_key(self, key):
        if len(key) != 66:
            raise Exception("Invalid key")
        return key

    async def get_balance(self, public_key):
        result = await self.rest.get_balance(public_key=self.validate_public_key(public_key))
        print(f'get_balance result: {result}')
        return result
