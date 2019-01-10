import hashlib

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import (
    padding,
    rsa,
    utils,
)

from remme.enums.key_type import KeyType
from remme.enums.remme_family_name import RemmeFamilyName
from remme.enums.rsa_signature_padding import RsaSignaturePadding
from remme.remme_keys.interface import IRemmeKeys
from remme.models.key_dto import KeyDto
from remme.remme_utils import (
    dict_to_base64,
    generate_address,
    private_key_to_pem,
    public_key_to_pem,
    utf8_to_bytes,
)


class RSA(KeyDto, IRemmeKeys):
    """
    RSA class implementation.

    References:
        - https://cryptography.io/en/latest/hazmat/primitives/asymmetric/rsa/
    """

    _rsa_key_size = 2048

    def __init__(self, private_key, public_key):
        """
        Constructor for RSA key pair. If only private key available then public key will be generate from private.
        :param private_key: (required)
        :param public_key: (optional)
        """
        super(RSA, self).__init__()

        if private_key and public_key:
            self._private_key = private_key
            self._public_key = public_key

        elif private_key:
            self._private_key = private_key
            self._public_key = self._private_key.public_key()

        elif public_key:
            self._public_key = public_key

        if self._private_key:
            self._private_key_pem = private_key_to_pem(self._private_key)

        self._public_key_pem = public_key_to_pem(self._public_key)

        self._address = generate_address(RemmeFamilyName.PUBLIC_KEY.value,  self._public_key_pem)
        self._key_type = KeyType.RSA

    @staticmethod
    def generate_key_pair(options=None):
        """
        Generate public and private key pair.
        :param options _rsa_key_size can be specified (optional)
        :return: generated key pair
        """
        if options is not None:
            private_key = rsa.generate_private_key(public_exponent=65537, key_size=options, backend=default_backend())
            return private_key, private_key.public_key()

        private_key = rsa.generate_private_key(
            public_exponent=65537, key_size=RSA._rsa_key_size, backend=default_backend(),
        )
        return private_key, private_key.public_key()

    @staticmethod
    def get_address_from_public_key(public_key):
        """
        Get address from public key.
        :param public_key object
        :return: address in blockchain generated from public key PEM string
        """
        return generate_address(RemmeFamilyName.PUBLIC_KEY.value, public_key_to_pem(public_key=public_key))

    def sign(self, data, rsa_signature_padding=None):
        """
        Sign provided data with selected key implementation.
        :param data: data string which will be signed
        :param rsa_signature_padding: RSA padding for signature (optional)
        :return: hex string for signature
        """
        if self._private_key is None:
            raise Exception('Private key is not provided!')

        if isinstance(data, str):
            data = utf8_to_bytes(data)

        if rsa_signature_padding:

            if rsa_signature_padding == RsaSignaturePadding.PSS:
                prehashed_msg = hashlib.sha256(data).digest()

                return self._private_key.sign(
                    data=prehashed_msg,
                    padding=padding.PSS(
                        mgf=padding.MGF1(hashes.SHA256()),
                        salt_length=padding.PSS.MAX_LENGTH,
                    ),
                    algorithm=utils.Prehashed(hashes.SHA256()),
                )

            if rsa_signature_padding == RsaSignaturePadding.PKCS1v15:
                prehashed_msg = hashlib.sha512(data).digest()

                return self._private_key.sign(
                    data=prehashed_msg,
                    padding=padding.PKCS1v15(),
                    algorithm=utils.Prehashed(hashes.SHA512()),
                )

        else:
            raise Exception('RSA signature padding is not provided!')

    def verify(self, data, signature, rsa_signature_padding=None):
        """
        Verify signature for selected key implementation.
        :param data: data string which will be verified
        :param signature: hex string of signature
        :param rsa_signature_padding: RSA padding for signature (optional)
        :return: none: in case signature is correct
        """
        if isinstance(data, str):
            data = utf8_to_bytes(data)

        if rsa_signature_padding:

            if rsa_signature_padding == RsaSignaturePadding.PSS:
                try:
                    prehashed_msg = hashlib.sha256(data).digest()

                    signature_verified = self._public_key.verify(
                        signature=signature,
                        data=prehashed_msg,
                        padding=padding.PSS(
                            mgf=padding.MGF1(hashes.SHA256()),
                            salt_length=padding.PSS.MAX_LENGTH
                        ),
                        algorithm=utils.Prehashed(hashes.SHA256()),
                    )

                    if signature_verified is None:
                        return True

                except InvalidSignature:
                    print('ERROR: Payload and/or signature failed verification!')

            if rsa_signature_padding == RsaSignaturePadding.PKCS1v15:

                try:
                    prehashed_msg = hashlib.sha512(data).digest()

                    signature_verified = self._public_key.verify(
                        signature=signature,
                        data=prehashed_msg,
                        padding=padding.PKCS1v15(),
                        algorithm=utils.Prehashed(hashes.SHA512()),
                    )

                    if signature_verified is None:
                        return True

                except InvalidSignature:
                    print('ERROR: Payload and/or signature files failed verification!')

        else:
            raise Exception('RSA signature padding is not provided!')
