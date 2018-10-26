from sawtooth_signing.secp256k1 import Secp256k1PrivateKey
from sawtooth_signing import create_context, CryptoFactory
from remme.remme_utils import hex_to_bytes, generate_address, RemmeFamilyName
import re


class RemmeAccount:

    _context = None
    _family_name = None
    _signer = None
    private_key_hex = None
    private_key = None
    public_key_hex = None
    public_key = None
    address = None

    @staticmethod
    def is_valid_private_hex(_private_hex):
        return re.match(r"^[0-9a-f]{64}$", _private_hex) is not None

    def __init__(self, private_key_hex):
        self._family_name = RemmeFamilyName.ACCOUNT.value[0]
        if private_key_hex and not self.is_valid_private_hex(private_key_hex):
            raise Exception("Invalid private key given!")
        self._context = create_context("secp256k1")
        if not private_key_hex:
            self.private_key = self._context.new_random_private_key()
        else:
            self.private_key = Secp256k1PrivateKey.from_hex(private_key_hex)

        self._signer = CryptoFactory(self._context).new_signer(self.private_key)
        self.private_key_hex = self.private_key.as_hex()
        self.public_key = self._signer.get_public_key()
        self.public_key_hex = self.public_key.as_hex()
        self.address = generate_address(self._family_name, self.public_key_hex)

    def sign(self, transaction):
        if type(transaction) == str:
            transaction = hex_to_bytes(transaction)
        return self._signer.sign(transaction)

    def verify(self, signature, transaction):
        return self._context.verify(signature, transaction, self.public_key)

    def get_family_name(self):
        return self._family_name

    def get_address(self):
        return self.address

    def get_public_key(self):
        return self.public_key

    def get_public_key_hex(self):
        return self.public_key_hex

    def get_private_key(self):
        return Secp256k1PrivateKey.from_hex(self.private_key_hex)

    def get_private_key_hex(self):
        return self.get_private_key_hex()
