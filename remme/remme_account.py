from sawtooth_signing.secp256k1 import Secp256k1PrivateKey
import sawtooth_signing
from remme.remme_utils import hex_to_bytes
from remme.remme_utils import generate_address
import re


class RemmeAccount:

    _family_name = None
    _signer = None
    private_hex_key = None
    public_hex_key = None
    address = None

    def __init__(self, private_key_hex):
        self._family_name = "account"
        if private_key_hex and not self.is_valid_private_hex(private_key_hex):
            raise Exception("Invalid private key given!")
        context = sawtooth_signing.create_context("secp256k1")
        if not private_key_hex:
            private_key = context.new_random_private_key()
        else:
            private_key = Secp256k1PrivateKey.from_hex(private_key_hex)
        self._signer = sawtooth_signing.CryptoFactory(context).new_signer(private_key)
        self.private_hex_key = private_key.as_hex()
        self.public_hex_key = self._signer.get_public_key().as_hex()
        self.address = generate_address(self._family_name, self.public_hex_key)

    @staticmethod
    def is_valid_private_hex(_private_hex):
        return re.match(r"^[0-9a-f]{64}$", _private_hex) is not None

    def sign(self, transaction):
        if type(transaction) == str:
            transaction = hex_to_bytes(transaction)
        return self._signer.sign(transaction)

    def get_private_key(self):
        return Secp256k1PrivateKey.from_hex(self.private_hex_key)