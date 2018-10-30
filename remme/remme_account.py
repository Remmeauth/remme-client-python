from sawtooth_signing.secp256k1 import Secp256k1PrivateKey
from sawtooth_signing import create_context, CryptoFactory
from remme.remme_utils import hex_to_bytes, generate_address, RemmeFamilyName, is_hex
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

    def __init__(self, private_key_hex):
        self._family_name = RemmeFamilyName.ACCOUNT.value
        if private_key_hex and re.match(RemmePatterns.PRIVATE_KEY.value, private_key_hex) is None:
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
        if isinstance(transaction, str) and is_hex(transaction):
            transaction = hex_to_bytes(transaction)
        if not isinstance(transaction, bytes):
            raise Exception("Invalid type of transaction")
        return self._signer.sign(transaction)

    def verify(self, signature, transaction):
        if not isinstance(transaction, bytes):
            raise Exception("Incorrect transaction type")
        if not isinstance(signature, str):
            raise Exception("Incorrect signature type")
        return self._context.verify(signature, transaction, self._public_key)

    @property
    def family_name(self):
        """
        Get constant account transaction's family name
        :return: {string}
        """
        return self._family_name

    @property
    def address(self):
        """
        Get address generated from public key hex
        :return: {bytes}
        """
        return self._address

    @property
    def public_key(self):
        """
        Get public key that that was generated from public key hex
        :return: {sawtooth_signing.secp256k1.Secp256k1PublicKey}
        """
        return self._public_key

    @property
    def public_key_hex(self):
        """
        Get public key hex that was generated automatically or given by user
        :return: {string}
        """
        return self._public_key_hex

    @property
    def private_key(self):
        """
        Get private key that was generated from user's public key
        :return: {sawtooth_signing.secp256k1.Secp256k1PrivateKey}
        """
        return self._private_key

    @property
    def private_key_hex(self):
        """
        Get private key hex that was generated from user's private key
        :return: {string}
        """
        return self._private_key_hex
