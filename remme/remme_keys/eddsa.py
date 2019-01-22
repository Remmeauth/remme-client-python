import hashlib
import os

import ed25519
from ed25519 import SigningKey, VerifyingKey

from remme.enums.key_type import KeyType
from remme.enums.remme_family_name import RemmeFamilyName
from remme.remme_keys.interface import IRemmeKeys
from remme.models.key_dto import KeyDto
from remme.remme_utils import (
    generate_address,
    utf8_to_bytes,
)


class EdDSA(KeyDto, IRemmeKeys):
    """
    EdDSA (ed25519) class implementation.

    References:
        - https://github.com/warner/python-ed25519
    """

    def __init__(self, private_key, public_key):
        """
        Constructor for EdDSA key pair.
        If only private key available then public key will be generate from private.
        :param private_key in bytes (required)
        :param public_key in bytes (optional)
        """
        super(EdDSA, self).__init__()

        if private_key and public_key:
            self._private_key = private_key
            self._public_key = public_key
            self._private_key_obj = SigningKey(self._private_key)
            self._public_key_obj = VerifyingKey(self._public_key)

        elif private_key:
            self._private_key = private_key
            self._private_key_obj = SigningKey(self._private_key)

            self._public_key_obj = self._private_key_obj.get_verifying_key()
            self._public_key = self._public_key_obj.to_bytes()

        elif public_key:
            self._public_key = public_key
            self._public_key_obj = VerifyingKey(self._public_key)

        if self._private_key:
            self._private_key_hex = self._private_key.hex()

        self._public_key_hex = self._public_key.hex()

        self._address = generate_address(
            _family_name=RemmeFamilyName.PUBLIC_KEY.value,
            _public_key_to=self._public_key,
        )
        self._key_type = KeyType.EdDSA

    @staticmethod
    def generate_key_pair(seed=None):
        """
        Generate public and private key pair.
        :param seed: bytes
        :return: generated key pair in bytes
        """
        if seed:
            private_key_obj, public_key_obj = ed25519.SigningKey(seed), ed25519.VerifyingKey(seed)
            return private_key_obj.to_bytes(), public_key_obj.to_bytes()

        private_key_obj, public_key_obj = ed25519.create_keypair(entropy=os.urandom)
        return private_key_obj.to_bytes(), public_key_obj.to_bytes()

    @staticmethod
    def get_address_from_public_key(public_key):
        """
        Get address from public key.
        :param public_key in bytes
        :return: address in blockchain generated from public key
        """
        return generate_address(RemmeFamilyName.PUBLIC_KEY.value, public_key)

    def sign(self, data, rsa_signature_padding=None):
        """
        Sign provided data with selected key implementation.
        :param data: data string which will be signed
        :param rsa_signature_padding: not used in EdDSA
        :return: hex string for signature
        """
        if self._private_key_obj is None:
            raise Exception('Private key is not provided!')

        if isinstance(data, str):
            data = utf8_to_bytes(data)

        return self._private_key_obj.sign(msg=hashlib.sha256(data).digest())

    def verify(self, data, signature, rsa_signature_padding=None):
        """
        Verify signature for selected key implementation.
        :param data: data string which will be verified
        :param signature: hex string of signature
        :param rsa_signature_padding: not used in EdDSA
        :return: none: in case signature is correct
        """
        if isinstance(data, str):
            data = utf8_to_bytes(data)

        try:
            self._public_key_obj.verify(
                sig=signature,
                msg=hashlib.sha256(data).digest(),
            )
            return True

        except ed25519.BadSignatureError:
            return False