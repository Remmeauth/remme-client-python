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
        """
        Args:
            network_config (dict): config of network (node address and ssl mode)
            batch_id (string): batch id
            certificate (optional): x509 certificate object
        """

        super(CertificateTransactionResponse, self).__init__(
            network_config=network_config, batch_id=batch_id,
        )
        self._certificate = certificate
        self._keys = RSA(
            private_key=private_key_to_der(self._certificate.private_key),
            public_key=public_key_to_der(self._certificate.public_key()),
        )

    @property
    def certificate(self):
        """
        Return x509 certificate object.
        """
        return self._certificate

    def sign(self, data, rsa_signature_padding=None):
        """
        Sign data with a certificate's private key and output DigestInfo DER-encoded bytes (default for PSS).

        Args:
            data (str): data string which will be signed
            rsa_signature_padding (RsaSignaturePadding, optional): RSA padding

        Returns:
            Hex string of signature.
        """
        return self._keys.sign(
            data=data,
            rsa_signature_padding=rsa_signature_padding,
        )

    def verify(self, data, signature, rsa_signature_padding=None):
        """
        Verify data with a public key.

        Args:
            data (str): data string which will be verified
            signature (str): hex string of signature
            rsa_signature_padding (RsaSignaturePadding, optional): RSA padding

        Returns:
            Boolean ``True`` if signature is correct, or ``False`` if invalid.
        """
        return self._keys.verify(
            data=data,
            signature=signature,
            rsa_signature_padding=rsa_signature_padding,
        )
