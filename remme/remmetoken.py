from remme.remmerest import RemmeRest

__author__ = 'dethline'


class RemmeToken:

    rest = None

    def __init__(self, network_config):
        self.rest = RemmeRest(network_config=network_config)

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

    def get_balance(self, public_key):
        valid_public_key = self.validate_public_key(public_key)
        url = f'/api/v1/token/{valid_public_key}'
        result = self.rest.get(url=url)
        if result['status'] == "OK":
            data = result['data']
            return data['balance']
        raise Exception("Failed to get balance")
