import base64

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import (
    hashes,
    serialization,
)
from cryptography.hazmat.primitives.asymmetric import (
    ec,
    utils,
)

from remme.constants.key_type import KeyType
from remme.constants.remme_family_name import RemmeFamilyName
from remme.keys.interface import IRemmeKeys
from remme.models.key_dto import KeyDto
from remme.remme_utils import (
    dict_to_base64,
    generate_address,
)


class ECDSA(KeyDto, IRemmeKeys):
    """
    ECDSA (secp256k1) class implementation.
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

        elif private_key:
            self._private_key = private_key
            private_key_obj = serialization.load_pem_private_key(
                self._private_key,
                password=None,
                backend=default_backend(),
            )
            public_key_obj = private_key_obj.public_key()

            self._public_key = public_key_obj.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo,
            )

        self._private_key_hex = self.private_key.encode('hex')
        self._public_key_hex = self._public_key.encode('hex')

        self._public_key_base64 = dict_to_base64(self._public_key_hex)
        self._address = generate_address(RemmeFamilyName.PUBLIC_KEY, self._public_key_base64)
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
        public_key_hex = public_key.encode('hex')
        public_key_base64 = dict_to_base64(public_key_hex)
        return generate_address(RemmeFamilyName.PUBLIC_KEY, public_key_base64)

    def sign(self, data):
        """
        Sign provided data with selected key implementation.
        :param data: data string which will be signed
        :return: hex string for signature
        """
        private_key = serialization.load_pem_private_key(
            data=self._private_key,
            password=None,
            backend=default_backend(),
        )

        chosen_hash = hashes.SHA256()
        hasher = hashes.Hash(chosen_hash, default_backend())
        hasher.update(data.encode('utf-8'))
        digest = hasher.finalize()

        signature = base64.b64encode(private_key.sign(
            digest,
            ec.ECDSA(utils.Prehashed(chosen_hash)),
        ))

        return signature

    def verify(self, data, signature):
        """
        Verify signature for selected key implementation.
        :param data: data string which will be verified
        :param signature: hex string of signature
        :return: none: in case signature is correct
        """
        public_key = serialization.load_pem_public_key(
            self._public_key,
            backend=default_backend(),
        )

        try:
            chosen_hash = hashes.SHA256()
            hasher = hashes.Hash(chosen_hash, default_backend())
            hasher.update(data.encode('utf-8'))
            digest = hasher.finalize()

            signature_verified = public_key.verify(
                base64.b64decode(signature),
                digest,
                ec.ECDSA(utils.Prehashed(chosen_hash)),
            )

            if signature_verified is None:
                print('Signature verified successfully!')

        except InvalidSignature:
            print('ERROR: Payload and/or signature failed verification!')
