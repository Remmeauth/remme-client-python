import os

import ed25519

from remme.enums.key_type import KeyType
from remme.enums.remme_family_name import RemmeFamilyName
from remme.keys.interface import IRemmeKeys
from remme.models.key_dto import KeyDto
from remme.remme_utils import (
    dict_to_base64,
    generate_address,
)


class EdDSA(KeyDto, IRemmeKeys):
    """
    EdDSA (ed25519) class implementation.

    References:
        - https://github.com/warner/python-ed25519
    """

    def __init__(self, private_key, public_key):
        """
        Constructor for EdDSA key pair. If only private key available then public key will be generate from private.
        :param private_key: (required)
        :param public_key: (optional)
        """
        super(EdDSA, self).__init__()

        if private_key and public_key:
            self._private_key = private_key
            self._public_key = public_key

            self._private_key_as_bytes = self._private_key.to_bytes()
            self._public_key_as_bytes = self._public_key.to_bytes()

        elif private_key:
            self._private_key = private_key
            self._public_key = self._private_key.get_verifying_key()

            self._private_key_as_bytes = self._private_key.to_bytes()
            self._public_key_as_bytes = self._public_key.to_bytes()

        elif public_key:
            self._public_key = public_key
            self._public_key_as_bytes = self._public_key.to_bytes()

        if self._private_key:
            self._private_key_hex = self._private_key_as_bytes.hex()

        self._public_key_hex = self._public_key_as_bytes.hex()

        self._public_key_base64 = dict_to_base64(self._public_key_hex).decode()
        self._address = generate_address(RemmeFamilyName.PUBLIC_KEY.value, self._public_key_base64)
        self._key_type = KeyType.EdDSA

    @staticmethod
    def generate_key_pair():
        """
        Generate public and private key pair.
        :return: generated key pair
        """
        private_key, public_key = ed25519.create_keypair(entropy=os.urandom)
        return private_key, public_key

    @staticmethod
    def get_address_from_public_key(public_key):
        """
        Get address from public key.
        :param public_key
        :return: address in blockchain generated from public key string
        """
        public_key_as_bytes = public_key.to_bytes()
        public_key_hex = public_key_as_bytes.hex()
        public_key_base64 = dict_to_base64(public_key_hex).decode()

        return generate_address(RemmeFamilyName.PUBLIC_KEY.value, public_key_base64)

    def sign(self, data, rsa_signature_padding=None):
        """
        Sign provided data with selected key implementation.
        :param data: data string which will be signed
        :param rsa_signature_padding: not used in EdDSA
        :return: hex string for signature
        """
        if self._private_key is None:
            raise Exception('Private key is not provided!')

        signature = self._private_key.sign(msg=data.encode())
        return signature.hex()

    def verify(self, data, signature, rsa_signature_padding=None):
        """
        Verify signature for selected key implementation.
        :param data: data string which will be verified
        :param signature: hex string of signature
        :param rsa_signature_padding: not used in EdDSA
        :return: none: in case signature is correct
        """
        try:
            signature_verified = self._public_key.verify(
                sig=bytes.fromhex(signature),
                msg=data.encode(),
            )

            if signature_verified is None:
                return 'Signature verified successfully!'

        except ed25519.BadSignatureError:
            print('ERROR: Payload and/or signature failed verification!')
