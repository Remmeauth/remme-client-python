import binascii

import secp256k1
from sawtooth_signing.secp256k1 import (
    __CTX__,
    Secp256k1Context,
    Secp256k1PrivateKey,
    Secp256k1PublicKey,
)

from remme.enums.key_type import KeyType
from remme.enums.remme_family_name import RemmeFamilyName
from remme.remme_keys.interface import IRemmeKeys
from remme.models.key_dto import KeyDto
from remme.remme_utils import (
    generate_address,
    utf8_to_bytes,
)


class ECDSA(KeyDto, IRemmeKeys):
    """
    ECDSA (secp256k1) class implementation.

    References:
        - https://github.com/hyperledger/sawtooth-core/
    """

    def __init__(self, private_key, public_key):
        """
        Constructor for ECDSA key pair. If only private key available then public key will be generate from private.
        :param private_key in bytes (required)
        :param public_key in bytes (optional)
        """
        super(ECDSA, self).__init__()

        if private_key and public_key:
            self._private_key = private_key
            self._public_key = public_key

            self._private_key_obj = self._private_key_bytes_to_object(private_key=self._private_key)
            self._public_key_obj = self._public_key_bytes_to_object(public_key=self._public_key)

        elif private_key:
            self._private_key = private_key

            self._private_key_obj = self._private_key_bytes_to_object(private_key=self._private_key)
            self._public_key_obj = Secp256k1PublicKey(self._private_key_obj.secp256k1_private_key.pubkey)

            self._public_key = self._public_key_obj.as_bytes()

        elif public_key:
            self._public_key = public_key
            self._public_key_obj = self._public_key_bytes_to_object(public_key=self._public_key)

        if self._private_key:
            self._private_key_hex = self._private_key.hex()

        self._public_key_hex = self._public_key.hex()

        self._address = generate_address(RemmeFamilyName.PUBLIC_KEY.value, self._public_key)
        self._key_type = KeyType.ECDSA

    @staticmethod
    def generate_key_pair():
        """
        Generate public and private key pair.
        :return: generated key pair in bytes
        """
        private_key_obj = Secp256k1PrivateKey.new_random()
        public_key_obj = Secp256k1PublicKey(private_key_obj.secp256k1_private_key.pubkey)

        return private_key_obj.as_bytes(), public_key_obj.as_bytes()

    @staticmethod
    def get_address_from_public_key(public_key):
        """
        Get address from public key.
        :param public_key in bytes
        :return: address in blockchain generated from public key string
        """
        return generate_address(
            _family_name=RemmeFamilyName.PUBLIC_KEY.value,
            _public_key_to=public_key,
        )

    def sign(self, data, rsa_signature_padding=None):
        """
        Sign provided data with selected key implementation.
        :param data: data string which will be signed
        :param rsa_signature_padding: not used in ECDSA
        :return: hex string for signature
        """
        if self._private_key is None:
            raise Exception('Private key is not provided!')

        if isinstance(data, str):
            data = utf8_to_bytes(data)

        sig = Secp256k1Context().sign(message=data, private_key=self._private_key_obj)
        return bytes.fromhex(sig)

    def verify(self, data, signature, rsa_signature_padding=None):
        """
        Verify signature for selected key implementation.
        :param data: data string which will be verified
        :param signature: hex string of signature
        :param rsa_signature_padding: not used in ECDSA
        :return: true: in case signature is correct
        """
        if isinstance(data, str):
            data = utf8_to_bytes(data)

        try:
            if isinstance(signature, bytes):
                signature = binascii.hexlify(signature).decode('utf-8')

            return Secp256k1Context().verify(signature, data, self._public_key_obj)

        except Exception:
            return False

    @staticmethod
    def _public_key_bytes_to_object(public_key):
        """
        Public key bytes to object.
        :param public_key in bytes
        :return: object
        """
        return Secp256k1PublicKey(secp256k1.PublicKey(public_key, raw=True, ctx=__CTX__))

    @staticmethod
    def _private_key_bytes_to_object(private_key):
        """
        Private key bytes to object.
        :param private_key in bytes
        :return: object
        """
        return Secp256k1PrivateKey(secp256k1.PrivateKey(private_key, ctx=__CTX__))
