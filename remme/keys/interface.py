import abc


class IRemmeKeys(metaclass=abc.ABCMeta):

    @staticmethod
    @abc.abstractmethod
    def get_public_key():
        pass

    @staticmethod
    @abc.abstractmethod
    def get_private_key():
        pass

    @staticmethod
    @abc.abstractmethod
    def get_key_type():
        pass

    @staticmethod
    @abc.abstractmethod
    def sign(data, rsa_signature_padding):
        """
        Sign provided data with selected key implementation.

        :param data: data string which will be signed
        :param rsa_signature_padding: RSA padding for signature (optional)
        :return: hex string for signature
        """
        pass

    @staticmethod
    @abc.abstractmethod
    def verify(data, signature, rsa_signature_padding):
        """
        Verify signature for selected key implementation.

        :param data: data string which will be verified
        :param signature: hex string of signature
        :param rsa_signature_padding: RSA padding for signature (optional)
        :return: true: in case signature is correct
        """
        pass
