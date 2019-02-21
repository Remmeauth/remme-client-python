"""
Base class for response on certificate creation.
"""
from remme.models.keys.rsa import RSA
from remme.models.transaction_service.base_transaction_response import BaseTransactionResponse
from remme.utils import (
    private_key_to_der,
    public_key_to_der,
)


class CertificateTransactionResponse(BaseTransactionResponse):

    def __init__(self, network_config, batch_id, certificate=None):

        super(CertificateTransactionResponse, self).__init__(
            network_config=network_config, batch_id=batch_id,
        )
        self._certificate = certificate
        self._keys = RSA(
            private_key=private_key_to_der(self._certificate.private_key),
            public_key=public_key_to_der(self._certificate.public_key()),
        )

    def sign(self, data, rsa_signature_padding=None):
        """
        Sign data with a certificate's private key and output DigestInfo DER-encoded bytes (default for PSS).
        :param data: string
        :param rsa_signature_padding: RsaSignaturePadding
        :return: hex string of signature
        """
        return self._keys.sign(
            data=data,
            rsa_signature_padding=rsa_signature_padding,
        )

    def verify(self, data, signature, rsa_signature_padding=None):
        """
        Verify data with a public key.
        :param data: string
        :param signature: string
        :param rsa_signature_padding: RsaSignaturePadding
        :return: True: boolean
        """
        return self._keys.verify(
            data=data,
            signature=signature,
            rsa_signature_padding=rsa_signature_padding,
        )
