import base64
import hashlib
import math
from enum import Enum

# from Crypto.PublicKey import RSA as crypto_rsa
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric.padding import calculate_max_pss_salt_length

from remme.enums.remme_family_name import RemmeFamilyName
from remme.enums.rsa_signature_padding import RsaSignaturePadding
from remme.keys.interface import IRemmeKeys
# from remme.models.key_dto import KeyDto
from remme.remme_utils import (
    generate_address,
    private_key_to_pem,
    public_key_to_pem,
)


class KeyType(Enum):
    RSA = 0


class RSA(IRemmeKeys):

    _rsa_key_size = 2048

    def __init__(self, private_key, public_key):
        """
        Constructor for RSA key pair. If only private key available then public key will be generate from private.
        :param private_key: (required)
        :param public_key: (optional)
        """
        if private_key and public_key:
            self.private_key = private_key
            self.public_key = public_key
        elif private_key:
            self.private_key = private_key
            self.public_key = private_key.publickey().exportKey('PEM')

        self.public_key_pem = public_key_to_pem(self.public_key)
        self.private_key_to_pem = private_key_to_pem(self.private_key)

        self.public_key_base64 = base64.b64encode(self.public_key_pem.encode('utf-8'))
        self.address = generate_address(RemmeFamilyName.PUBLIC_KEY, self.public_key_pem)
        self.key_type = KeyType.RSA

    def generate_key_pair(self, options):
        """
        Generate public and private key pair.
        :param options _rsa_key_size can be specified (optional)
        :return: generated key pair
        """
        # rsa.generate_private_key(public_exponent=65537, key_size=2048, backend=default_backend())
        if not options:
            return crypto_rsa.generate(bits=self._rsa_key_size)

        return crypto_rsa.generate(bits=options)  # what is return?
        # private_key = key.exportKey()
        # public_key = key.publickey().exportKey()

    @staticmethod
    def get_address_from_public_key(public_key):
        """
        Get address from public key.
        :param public_key
        :return: address in blockchain generated from public key PEM string
        """
        return generate_address(RemmeFamilyName.PUBLIC_KEY, public_key_to_pem(public_key=public_key))

    def _calculat_salt_length(self, message_digest):
        calculate_max_pss_salt_length(key=self._rsa_key_size, hash_algorithm=message_digest)
        emlen = math.ceil(self._rsa_key_size / 8)
        return emlen - message_digest.digest_size - 2

    def sign(self, data, rsa_signature_padding):
        """
        Create signature for data.
        :param data:
        :param rsa_signature_padding:
        :return: signed signature
        """
        # message_digest = hashlib.sha512()
        # message_digest.update(data.encode('utf-8'))
        # signature = ''

        if RsaSignaturePadding.PSS:

            return base64.b64encode(key.sign(
                data,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA512()),
                    salt_length=padding.PSS.MAX_LENGTH),
                  # padding.PKCS1v15(),
                hashes.SHA512()
                )
            ).decode()

        if RsaSignaturePadding.PKCS1v15:
            return base64.b64encode(key.sign(
                data,
                padding.PKCS1v15(),
                hashes.SHA512()
                )
            ).decode()

    def verify(self, data, signature, rsa_signature_padding):
        message_digest = hashlib.sha512()
        message_digest.update(data.encode('utf-8'))

        if RsaSignaturePadding.PSS:
            try:
                return public_key.verify(
                    base64.b64decode(signature),
                    data.encode('utf-8'),
                    padding.PSS(
                        mgf=padding.MGF1(hashes.SHA512()),
                        salt_length=padding.PSS.MAX_LENGTH),
                    # padding.PKCS1v15(),
                    hashes.SHA512(),
                    # utils.Prehashed(chosen_hash)
                )
            except InvalidSignature as e:
                print('ERROR: Payload and/or signature files failed verification!')

        if RsaSignaturePadding.PKCS1v15:
            try:
                return public_key.verify(
                    base64.b64decode(signature),
                    data.encode('utf-8'),
                    padding.PKCS1v15(),
                    hashes.SHA512(),
                    # utils.Prehashed(chosen_hash)
                )
            except InvalidSignature as e:
                print('ERROR: Payload and/or signature files failed verification!')

        # if RsaSignaturePadding.PSS:
        #     return self.public_key.verify(
        #         signature,
        #         message_digest,
        #         padding.PSS(
        #             mgf=padding.MGF1(hashes.SHA512()),
        #             salt_length=padding.PSS.MAX_LENGTH,
        #         ),
        #         hashes.SHA512()
        #     )
        #
        # if RsaSignaturePadding.PKCS1v15:
        #     return self.public_key.verify(
        #         signature,
        #         message_digest,
        #         padding.PKCS1v15(),
        #         hashes.SHA512()
        #     )
