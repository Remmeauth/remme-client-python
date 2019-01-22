from cryptography.x509 import CertificateBuilder


class X509CertificateBuilder(CertificateBuilder):
    """
    Class for working with X509 certificate.
    """

    def __init__(self, private_key, **kwargs):
        super(X509CertificateBuilder, self).__init__(**kwargs)
        self._private_key = private_key

    @property
    def private_key(self):
        return self._private_key
