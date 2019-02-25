import binascii

import secp256k1
from sawtooth_signing.secp256k1 import (
    __CTX__,
    Secp256k1Context,
    Secp256k1PrivateKey,
    Secp256k1PublicKey,
)

from remme.models.interfaces.keys import IRemmeKeys
from remme.models.keys.key_dto import KeyDto
from remme.models.keys.key_type import KeyType
from remme.models.utils.family_name import RemmeFamilyName
from remme.utils import (
    generate_address,
    utf8_to_bytes,
)


class ECDSA(KeyDto, IRemmeKeys):
    """
    ``ECDSA (secp256k1)`` class implementation.

    References::
        - https://github.com/hyperledger/sawtooth-core/
    """

    def __init__(self, private_key=None, public_key=None):
        """
        Constructor for ``ECDSA`` key pair. If only private key available then public key will be generate from private.

        Args:
            private_key (bytes): secp256k1 private key
            public_key (bytes, optional): secp256k1 public key
        """
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

        if private_key:
            self._private_key_hex = self._private_key.hex()
        else:
            self._private_key_hex = None

        self._public_key_hex = self._public_key.hex()

        self._address = generate_address(RemmeFamilyName.PUBLIC_KEY.value, self._public_key)
        self._key_type = KeyType.ECDSA

        super(ECDSA, self).__init__(
            private_key=private_key if private_key else None, public_key=self._public_key,
            private_key_hex=self._private_key_hex, public_key_hex=self._public_key_hex,
            key_type=self._key_type, address=self._address,
        )

    @staticmethod
    def generate_key_pair():
        """
        Generate public and private key pair.

        Returns:
            Generated key pair in bytes.
        """
        private_key_obj = Secp256k1PrivateKey.new_random()
        public_key_obj = Secp256k1PublicKey(private_key_obj.secp256k1_private_key.pubkey)

        return private_key_obj.as_bytes(), public_key_obj.as_bytes()

    @staticmethod
    def get_address_from_public_key(public_key):
        """
        Get address from public key.

        Args:
            public_key (bytes): public key in bytes

        Returns:
            Address in blockchain generated from public key string.
        """
        return generate_address(
            _family_name=RemmeFamilyName.PUBLIC_KEY.value,
            _public_key_to=public_key,
        )

    def sign(self, data, rsa_signature_padding=None):
        """
        Sign provided data with selected key implementation.

        Args:
            data (str): data string which will be signed
            rsa_signature_padding (RsaSignaturePadding, optional): not used in ECDSA

        Returns:
            Hex string of signature.
        """
        if self._private_key is None:
            raise Exception('Private key is not provided!')

        if isinstance(data, str):
            data = utf8_to_bytes(data)

        sig = Secp256k1Context().sign(message=data, private_key=self._private_key_obj)
        return sig

    def verify(self, data, signature, rsa_signature_padding=None):
        """
        Verify signature for selected key implementation.

        Args:
            data (str): data string which will be verified
            signature (str): hex string of signature
            rsa_signature_padding (RsaSignaturePadding, optional): not used in ECDSA

        Returns:
            Boolean ``True`` if signature is correct, or ``False`` if invalid.
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

        Args:
            public_key (bytes): secp256k1 public key in bytes

        Returns:
            public key object
        """
        return Secp256k1PublicKey(secp256k1.PublicKey(public_key, raw=True, ctx=__CTX__))

    @staticmethod
    def _private_key_bytes_to_object(private_key):
        """
        Private key bytes to object.

        Args:
            private_key (bytes): secp256k1 private key in bytes

        Returns:
            private key key object
        """
        return Secp256k1PrivateKey(secp256k1.PrivateKey(private_key, ctx=__CTX__))
