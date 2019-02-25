import hashlib
import os

import ed25519
from ed25519 import SigningKey, VerifyingKey

from remme.models.interfaces.keys import IRemmeKeys
from remme.models.keys.key_dto import KeyDto
from remme.models.keys.key_type import KeyType
from remme.models.utils.family_name import RemmeFamilyName
from remme.utils import (
    generate_address,
    utf8_to_bytes,
)


class EdDSA(KeyDto, IRemmeKeys):
    """
    EdDSA (ed25519) class implementation.

    References::
        - https://github.com/warner/python-ed25519
    """

    def __init__(self, private_key, public_key):
        """
        Constructor for EdDSA key pair.
        If only private key available then public key will be generate from private.

        Args:
            private_key (bytes): ed25519 private key
            public_key (bytes, optional): ed25519 public key
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

        Args:
            seed (bytes, optional): seed

        Returns:
            Generated key pair in bytes.
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
        Args:
            public_key (bytes): public key in bytes

        Returns:
            Address in blockchain generated from public key string.
        """
        return generate_address(RemmeFamilyName.PUBLIC_KEY.value, public_key)

    def sign(self, data, rsa_signature_padding=None):
        """
        Sign provided data with selected key implementation.

        Args:
            data (str): data string which will be signed
            rsa_signature_padding (RsaSignaturePadding, optional): not used in EdDSA

        Returns:
            Hex string of signature.
        """
        if self._private_key_obj is None:
            raise Exception('Private key is not provided!')

        if isinstance(data, str):
            data = utf8_to_bytes(data)

        return self._private_key_obj.sign(msg=hashlib.sha256(data).digest())

    def verify(self, data, signature, rsa_signature_padding=None):
        """
        Verify signature for selected key implementation.

        Args:
            data (str): data string which will be verified
            signature (str): hex string of signature
            rsa_signature_padding (RsaSignaturePadding, optional): not used in EdDSA

        Returns:
            Boolean ``True`` if signature is correct, or ``False`` if invalid.
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
