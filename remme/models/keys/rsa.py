import hashlib

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import (
    padding,
    rsa,
    utils,
)

from remme.models.interfaces.keys import IRemmeKeys
from remme.models.keys.key_dto import KeyDto
from remme.models.keys.key_type import KeyType
from remme.models.keys.rsa_signature_padding import RsaSignaturePadding
from remme.models.utils.family_name import RemmeFamilyName
from remme.utils import (
    generate_address,
    private_key_to_der,
    public_key_to_der,
    private_key_der_to_object,
    public_key_der_to_object,
    utf8_to_bytes,
)


class RSA(KeyDto, IRemmeKeys):
    """
    RSA class implementation.

    References::
        - https://cryptography.io/en/latest/hazmat/primitives/asymmetric/rsa/
    """

    _rsa_key_size = 2048

    def __init__(self, private_key=None, public_key=None):
        """
        Constructor for RSA key pair. If only private key available then public key will be generate from private.

        Args:
            private_key (bytes): rsa private key
            public_key (bytes, optional): rsa public key
        """
        super(RSA, self).__init__()

        if private_key and public_key:
            self._private_key = private_key
            self._public_key = public_key
            self._private_key_obj = private_key_der_to_object(private_key=self._private_key)
            self._public_key_obj = public_key_der_to_object(public_key=self._public_key)

        elif private_key:
            self._private_key = private_key
            self._private_key_obj = private_key_der_to_object(private_key=self._private_key)
            self._public_key_obj = self._private_key_obj.public_key()
            self._public_key = public_key_to_der(public_key=self._public_key_obj)

        elif public_key:
            self._public_key = public_key
            self._public_key_obj = public_key_der_to_object(public_key=self._public_key)

        if self._private_key:
            self._private_key_hex = self._private_key.hex()

        self._public_key_hex = self._public_key.hex()

        self._address = generate_address(RemmeFamilyName.PUBLIC_KEY.value,  self._public_key)
        self._key_type = KeyType.RSA

    @staticmethod
    def generate_key_pair(options=None):
        """
        Generate public and private key pair.

        Args:
            options (integer): _rsa_key_size can be specified

        Returns:
            Generated key pair in bytes.
        """
        if options is not None:
            private_key = rsa.generate_private_key(public_exponent=65537, key_size=options, backend=default_backend())
            return private_key_to_der(private_key), public_key_to_der(private_key.public_key())

        private_key = rsa.generate_private_key(
            public_exponent=65537, key_size=RSA._rsa_key_size, backend=default_backend(),
        )
        return private_key_to_der(private_key), public_key_to_der(private_key.public_key())

    @staticmethod
    def get_address_from_public_key(public_key):
        """
        Get address from public key.

        Args:
            public_key (bytes): public key in bytes

        Returns:
            Address in blockchain generated from public key DER format.
        """
        return generate_address(RemmeFamilyName.PUBLIC_KEY.value, public_key)

    def sign(self, data, rsa_signature_padding=RsaSignaturePadding.PSS):
        """
        Sign provided data with selected key implementation.

        Args:
            data (str): data string which will be signed
            rsa_signature_padding (RsaSignaturePadding, optional): RSA padding for signature

        Returns:
            Hex string of signature.
        """
        if self._private_key is None:
            raise Exception('Private key is not provided!')

        if isinstance(data, str):
            data = utf8_to_bytes(data)

        if rsa_signature_padding:

            if rsa_signature_padding == RsaSignaturePadding.PSS:
                prehashed_msg = hashlib.sha256(data).digest()

                return self._private_key_obj.sign(
                    data=prehashed_msg,
                    padding=padding.PSS(
                        mgf=padding.MGF1(hashes.SHA256()),
                        salt_length=padding.PSS.MAX_LENGTH,
                    ),
                    algorithm=utils.Prehashed(hashes.SHA256()),
                )

            if rsa_signature_padding == RsaSignaturePadding.PKCS1v15:
                prehashed_msg = hashlib.sha256(data).digest()

                return self._private_key_obj.sign(
                    data=prehashed_msg,
                    padding=padding.PKCS1v15(),
                    algorithm=utils.Prehashed(hashes.SHA256()),
                )

    def verify(self, data, signature, rsa_signature_padding=RsaSignaturePadding.PSS):
        """
        Verify signature for selected key implementation.

        Args:
            data (str): data string which will be verified
            signature (str): hex string of signature
            rsa_signature_padding (RsaSignaturePadding, optional): RSA padding for signature

        Returns:
            Boolean ``True`` if signature is correct, or ``False`` if invalid.
        """
        if isinstance(data, str):
            data = utf8_to_bytes(data)

        if rsa_signature_padding:

            if rsa_signature_padding == RsaSignaturePadding.PSS:

                try:
                    prehashed_msg = hashlib.sha256(data).digest()

                    self._public_key_obj.verify(
                        signature=signature,
                        data=prehashed_msg,
                        padding=padding.PSS(
                            mgf=padding.MGF1(hashes.SHA256()),
                            salt_length=padding.PSS.MAX_LENGTH
                        ),
                        algorithm=utils.Prehashed(hashes.SHA256()),
                    )
                    return True

                except InvalidSignature:
                    return False

            if rsa_signature_padding == RsaSignaturePadding.PKCS1v15:

                try:
                    prehashed_msg = hashlib.sha256(data).digest()

                    self._public_key_obj.verify(
                        signature=signature,
                        data=prehashed_msg,
                        padding=padding.PKCS1v15(),
                        algorithm=utils.Prehashed(hashes.SHA256()),
                    )
                    return True

                except InvalidSignature:
                    return False
