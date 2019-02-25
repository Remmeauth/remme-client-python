import abc


class IRemmeTransactionService(metaclass=abc.ABCMeta):

    @staticmethod
    @abc.abstractmethod
    def create(family_name, family_version, inputs, outputs, payload_bytes):
        """
        Create transactions.

        Args:
            family_name (string): enum RemmeFamilyName
            family_version (string): family version
            inputs (list): list of input address
            outputs (list): list of output address
            payload_bytes (bytes): payload bytes
        """
        pass

    @staticmethod
    @abc.abstractmethod
    def send(payload):
        """
        Send transactions.

        Args:
            payload (bytes): transaction in base64
        """
        pass
