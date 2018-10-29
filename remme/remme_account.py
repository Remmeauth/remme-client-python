from sawtooth_signing.secp256k1 import Secp256k1PrivateKey
from sawtooth_signing import create_context, CryptoFactory
from remme.remme_utils import hex_to_bytes, generate_address, RemmeFamilyName
from remme.remme_patterns import RemmePatterns
import re


class RemmeAccount:

    _context = None
    _family_name = None
    _signer = None
    _private_key_hex = None
    _private_key = None
    _public_key_hex = None
    _public_key = None
    _address = None

    @staticmethod
    def is_valid_private_hex(_private_hex):
        return re.match(RemmePatterns.PRIVATE_KEY.value, _private_hex) is not None

    def __init__(self, private_key_hex):
        self._family_name = RemmeFamilyName.ACCOUNT.value[0]
        if private_key_hex and not self.is_valid_private_hex(private_key_hex):
            raise Exception("Invalid private key given!")
        self._context = create_context("secp256k1")
        if not private_key_hex:
            self._private_key = self._context.new_random_private_key()
        else:
            self._private_key = Secp256k1PrivateKey.from_hex(private_key_hex)

        self._signer = CryptoFactory(self._context).new_signer(self._private_key)
        self._private_key_hex = self._private_key.as_hex()
        self._private_key = Secp256k1PrivateKey.from_hex(self._private_key_hex)
        self._public_key = self._signer.get_public_key()
        self._public_key_hex = self._public_key.as_hex()
        self._address = generate_address(self._family_name, self._public_key_hex)

    def sign(self, transaction):
        if type(transaction) == str:
            transaction = hex_to_bytes(transaction)
        return self._signer.sign(transaction)

    def verify(self, signature, transaction):
        if not isinstance(transaction, bytes):
            raise Exception("Incorrect transaction type")
        if not isinstance(signature, str):
            raise Exception("Incorrect signature type")
        return self._context.verify(signature, transaction, self._public_key)

    @property
    def family_name(self):
        return self._family_name

    @property
    def address(self):
        return self._address

    @property
    def public_key(self):
        return self._public_key

    @property
    def public_key_hex(self):
        return self._public_key_hex

    @property
    def private_key(self):
        return self._private_key

    @property
    def private_key_hex(self):
        return self._private_key_hex
