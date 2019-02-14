import abc


class IRemmeCertificate(metaclass=abc.ABCMeta):

    @staticmethod
    @abc.abstractmethod
    def create(certificate_data_to_create):
        """
        Create certificate.

        :param certificate_data_to_create: dict
        :return: signed certificate object
        """
        pass

    @staticmethod
    @abc.abstractmethod
    def create_and_store(certificate_data_to_create):
        """
        Method that creates certificate and stores it in to REMChain.
        Send transaction to chain.

        :param certificate_data_to_create: dict
        :return: information about storing public key to REMChain
        """
        pass

    @staticmethod
    @abc.abstractmethod
    def store(certificate):
        """
        Store your certificate public key and hash of certificate into REMChain.
        Your certificate should contains private and public keys.
        Send transaction to chain.

        :param certificate: object
        :return: information about storing public key to REMChain
        """
        pass

    @staticmethod
    @abc.abstractmethod
    def check(certificate):
        """
        Check certificate's public key on validity and revocation.

        :param certificate: object
        :return: boolean
        """
        pass

    @staticmethod
    @abc.abstractmethod
    def get_info(certificate):
        """
        Get info about certificate's public key.

        :param certificate: object
        :return: information about public key
        """
        pass

    @staticmethod
    @abc.abstractmethod
    def revoke(certificate):
        """
        Revoke certificate's public key into REMChain.

        Send transaction to chain.
        :param certificate: object
        :return:
        """
        pass

    @staticmethod
    @abc.abstractmethod
    def sign(certificate, data, rsa_signature_padding):
        """
        Sign data with a certificate's private key and output DigestInfo DER-encoded bytes (default for PSS).

        :param certificate: object
        :param data: string
        :param rsa_signature_padding: RsaSignaturePadding
        :return: string
        """
        pass

    @staticmethod
    @abc.abstractmethod
    def verify(certificate, data, signature, rsa_signature_padding):
        """
        Verify data with a public key (default for PSS).

        :param certificate: object
        :param data: string
        :param signature: string
        :param rsa_signature_padding: RsaSignaturePadding
        :return: boolean
        """
        pass
