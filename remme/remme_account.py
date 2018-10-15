from remme.remme_utils import hex_to_bytes

sawtooth_signing = __import__('sawtooth-signing')


class RemmeAccount:

    _signer = None
    private_hex_key = None
    public_hex_key = None
    address = None

    def __init__(self, private_hex):
        pass

    def sign(self, transaction):
        if type(transaction) == str:
            transaction = hex_to_bytes(transaction)
        return self._signer.sign(transaction)
