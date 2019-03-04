import abc


class IRemmeKeys(metaclass=abc.ABCMeta):

    @staticmethod
    @abc.abstractmethod
    def sign(data, rsa_signature_padding=None):
        """
        Sign provided data with selected key implementation.

        Args:
            data (str): data string which will be signed
            rsa_signature_padding (RsaSignaturePadding, optional): used in RSA
        """
        pass

    @staticmethod
    @abc.abstractmethod
    def verify(data, signature, rsa_signature_padding=None):
        """
        Verify signature for selected key implementation.

        Args:
            data (str): data string which will be verified
            signature (str): hex string of signature
            rsa_signature_padding (RsaSignaturePadding, optional): used in RSA
        """
        pass
