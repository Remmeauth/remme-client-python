from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import (
    ec,
    utils,
)

from remme.enums.key_type import KeyType
from remme.enums.remme_family_name import RemmeFamilyName
from remme.keys.interface import IRemmeKeys
from remme.models.key_dto import KeyDto
from remme.remme_utils import (
    dict_to_base64,
    generate_address,
)


class ECDSA(KeyDto, IRemmeKeys):
    """
    ECDSA (secp256k1) class implementation.

    References:
        - https://cryptography.io/en/latest/hazmat/primitives/asymmetric/ec/
    """

    def __init__(self, private_key, public_key):
        """
        Constructor for ECDSA key pair. If only private key available then public key will be generate from private.
        :param private_key: (required)
        :param public_key: (optional)
        """
        super(ECDSA, self).__init__()

        if private_key and public_key:
            self._private_key = private_key
            self._public_key = public_key

            self.private_key_as_bytes = self.private_key_to_bytes(private_key=self._private_key)
            self.public_key_as_bytes = self.public_key_to_bytes(public_key=self._public_key)

        elif private_key:
            self._private_key = private_key
            self._public_key = self._private_key.public_key()

            self.private_key_as_bytes = self.private_key_to_bytes(private_key=self._private_key)
            self.public_key_as_bytes = self.public_key_to_bytes(public_key=self._public_key)

        elif public_key:
            self._public_key = public_key
            self.public_key_as_bytes = self.public_key_to_bytes(public_key=public_key)

        if self._private_key:
            self._private_key_hex = self.private_key_as_bytes.hex()

        self._public_key_hex = self.public_key_as_bytes.hex()

        self._address = generate_address(RemmeFamilyName.PUBLIC_KEY.value, self.public_key_as_bytes)
        self._key_type = KeyType.ECDSA

    @staticmethod
    def generate_key_pair():
        """
        Generate public and private key pair.
        :return: generated key pair
        """
        private_key = ec.generate_private_key(
            curve=ec.SECP256K1,
            backend=default_backend(),
        )
        public_key = private_key.public_key()

        return private_key, public_key

    @staticmethod
    def get_address_from_public_key(public_key):
        """
        Get address from public key.
        :param public_key
        :return: address in blockchain generated from public key string
        """
        public_key_as_bytes = ECDSA.public_key_to_bytes(public_key=public_key)

        return generate_address(
            _family_name=RemmeFamilyName.PUBLIC_KEY.value,
            _public_key_to=public_key_as_bytes,
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

        chosen_hash = hashes.SHA256()
        hasher = hashes.Hash(chosen_hash, default_backend())
        hasher.update(data.encode('utf-8'))
        digest = hasher.finalize()

        return self._private_key.sign(
            digest,
            ec.ECDSA(utils.Prehashed(chosen_hash)),
        ).hex()

    def verify(self, data, signature, rsa_signature_padding=None):
        """
        Verify signature for selected key implementation.
        :param data: data string which will be verified
        :param signature: hex string of signature
        :param rsa_signature_padding: not used in ECDSA
        :return: none: in case signature is correct
        """
        try:
            chosen_hash = hashes.SHA256()
            hasher = hashes.Hash(chosen_hash, default_backend())
            hasher.update(data.encode('utf-8'))
            digest = hasher.finalize()

            signature_verified = self._public_key.verify(
                bytes.fromhex(signature),
                digest,
                ec.ECDSA(utils.Prehashed(chosen_hash)),
            )

            if signature_verified is None:
                print('Signature verified successfully!')

        except InvalidSignature:
            print('ERROR: Payload and/or signature failed verification!')

    @staticmethod
    def public_key_to_bytes(public_key, compressed=False):
        """
        Public key object to bytes.
        :param public_key
        :param compressed: 0x02 and 0x03 = compressed, 0x04 = uncompressed
        :return: bytes
        """
        x_numbers = public_key.public_numbers().x
        y_numbers = public_key.public_numbers().y

        x_bytes = x_numbers.to_bytes(32, 'big')
        y_bytes = y_numbers.to_bytes(32, 'big')

        if compressed:
            compression_byte = b'\x03' if y_numbers & 1 else b'\x02'
            return compression_byte + x_bytes

        else:
            return b'\x04' + x_bytes + y_bytes

    @staticmethod
    def private_key_to_bytes(private_key):
        """
        Private key object to bytes.
        :param private_key
        :return: bytes
        """
        return private_key.private_numbers().private_value.to_bytes(32, 'big')
