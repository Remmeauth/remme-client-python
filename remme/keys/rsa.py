import base64

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import (
    padding,
    rsa,
)
from cryptography.hazmat.primitives.asymmetric.padding import calculate_max_pss_salt_length

from remme.enums.key_type import KeyType
from remme.enums.remme_family_name import RemmeFamilyName
from remme.enums.rsa_signature_padding import RsaSignaturePadding
from remme.keys.interface import IRemmeKeys
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

        self._public_key_base64 = dict_to_base64(self._public_key_pem)
        self._address = generate_address(RemmeFamilyName.PUBLIC_KEY, self._public_key_pem)
        self._key_type = KeyType.RSA

    def generate_key_pair(self, options=None):
        """
        Generate public and private key pair.
        :param options _rsa_key_size can be specified (optional)
        :return: generated key pair
        """
        if options is not None:
            return rsa.generate_private_key(public_exponent=65537, key_size=options, backend=default_backend())

        return rsa.generate_private_key(public_exponent=65537, key_size=self._rsa_key_size, backend=default_backend())

    @staticmethod
    def get_address_from_public_key(public_key):
        """
        Get address from public key.
        :param public_key object
        :return: address in blockchain generated from public key PEM string
        """
        return generate_address(RemmeFamilyName.PUBLIC_KEY, public_key_to_pem(public_key=public_key))

    def sign(self, data, rsa_signature_padding=None):
        """
        Sign provided data with selected key implementation.
        :param data: data string which will be signed
        :param rsa_signature_padding: RSA padding for signature (optional)
        :return: hex string for signature
        """
        if self._private_key is None:
            raise Exception('Private key is not provided!')

        chosen_hash = hashes.SHA512()
        hasher = hashes.Hash(chosen_hash, default_backend())
        hasher.update(utf8_to_bytes(_string=data))
        digest = hasher.finalize()

        if rsa_signature_padding:

            if rsa_signature_padding == RsaSignaturePadding.PSS:

                return base64.b64encode(self._private_key.sign(
                    digest,
                    padding.PSS(
                        mgf=padding.MGF1(hashes.SHA512()),
                        salt_length=self._calculate_salt_length(key=self._private_key)),
                    hashes.SHA512()
                    )
                ).decode()

            if rsa_signature_padding == RsaSignaturePadding.PKCS1v15:

                return base64.b64encode(self._private_key.sign(
                    digest,
                    padding.PKCS1v15(),
                    hashes.SHA512()
                )).decode()

        raise Exception('RSA signature padding is not provided!')

    def verify(self, data, signature, rsa_signature_padding=None):
        """
        Verify signature for selected key implementation.
        :param data: data string which will be verified
        :param signature: hex string of signature
        :param rsa_signature_padding: RSA padding for signature (optional)
        :return: none: in case signature is correct
        """
        chosen_hash = hashes.SHA512()
        hasher = hashes.Hash(chosen_hash, default_backend())
        hasher.update(utf8_to_bytes(_string=data))
        digest = hasher.finalize()

        if rsa_signature_padding:

            if rsa_signature_padding == RsaSignaturePadding.PSS:
                try:
                    signature_verified = self._public_key.verify(
                        base64.b64decode(signature),
                        digest,
                        padding.PSS(
                            mgf=padding.MGF1(hashes.SHA512()),
                            salt_length=self._calculate_salt_length(key=self._public_key)),
                        hashes.SHA512(),
                    )

                    if signature_verified is None:
                        print('Signature verified successfully!')

                except InvalidSignature:
                    print('ERROR: Payload and/or signature failed verification!')

            if rsa_signature_padding == RsaSignaturePadding.PKCS1v15:
                try:
                    signature_verified = self._public_key.verify(
                        base64.b64decode(signature),
                        digest,
                        padding.PKCS1v15(),
                        hashes.SHA512(),
                    )

                    if signature_verified is None:
                        print('Signature verified successfully!')

                except InvalidSignature:
                    print('ERROR: Payload and/or signature files failed verification!')

        raise Exception('RSA signature padding is not provided!')

    @staticmethod
    def _calculate_salt_length(key):
        """
        Calculate max PSS salt length.
        :param key: RSA public or private key object
        :return: integer
        """
        return calculate_max_pss_salt_length(key=key, hash_algorithm=hashes.SHA512())
