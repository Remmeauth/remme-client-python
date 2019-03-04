import abc


class IRemmeCertificate(metaclass=abc.ABCMeta):

    @staticmethod
    @abc.abstractmethod
    def create(certificate_data_to_create):
        """
        Create certificate.

        Args:
            certificate_data_to_create (kwargs): certificate data
        """
        pass

    @staticmethod
    @abc.abstractmethod
    def create_and_store(certificate_data_to_create):
        """
        Method that creates certificate and stores it in to REMChain.
        Send transaction to chain.

        Args:
            certificate_data_to_create (kwargs): certificate data
        """
        pass

    @staticmethod
    @abc.abstractmethod
    def store(certificate):
        """
        Store your certificate public key and hash of certificate into REMChain.
        Your certificate should contains private and public keys.
        Send transaction to chain.

        Args:
            certificate (object): certificate object
        """
        pass

    @staticmethod
    @abc.abstractmethod
    def check(certificate):
        """
        Check certificate's public key on validity and revocation.

        Args:
            certificate (object): certificate object
        """
        pass

    @staticmethod
    @abc.abstractmethod
    def get_info(certificate):
        """
        Get info about certificate's public key.

        Args:
            certificate (object): certificate object
        """
        pass

    @staticmethod
    @abc.abstractmethod
    def revoke(certificate):
        """
        Revoke certificate's public key into REMChain.
        Send transaction to chain.

        Args:
            certificate (object): certificate object
        """
        pass

    @staticmethod
    @abc.abstractmethod
    def sign(certificate, data, rsa_signature_padding):
        """
        Sign data with a certificate's private key and output DigestInfo DER-encoded bytes (default for PSS).

        Args:
            certificate (object): certificate object
            data (string): data string which will be signed
            rsa_signature_padding (RsaSignaturePadding): RSA padding
        """
        pass

    @staticmethod
    @abc.abstractmethod
    def verify(certificate, data, signature, rsa_signature_padding):
        """
        Verify data with a public key (default for PSS).

        Args:
            certificate (object): certificate object
            data (string): data string which will be verified
            signature (string): hex string of signature
            rsa_signature_padding (RsaSignaturePadding): RSA padding
        """
        pass
