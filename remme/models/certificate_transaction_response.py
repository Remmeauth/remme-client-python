"""
Base class for response on certificate creation.
"""
from remme.models.base_transaction_response import BaseTransactionResponse
from remme.remme_keys.rsa import RSA


class CertificateTransactionResponse(BaseTransactionResponse):

    def __init__(self, node_address, ssl_mode, batch_id, certificate=None):

        super(CertificateTransactionResponse, self).__init__(
            node_address=node_address, ssl_mode=ssl_mode, batch_id=batch_id,
        )
        self._certificate = certificate
        self._keys = RSA(
            private_key=self._certificate.private_key,
            public_key=self._certificate.public_key,
        )

    def sign(self, data, rsa_signature_padding=None):
        """
        Sign data with a certificate's private key and output DigestInfo DER-encoded bytes (default for PSS).
        :param data: string
        :param rsa_signature_padding: RsaSignaturePadding
        :return: hex string for signature
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
