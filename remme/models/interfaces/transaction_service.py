import abc


class IRemmeTransactionService(metaclass=abc.ABCMeta):

    @staticmethod
    @abc.abstractmethod
    def create(family_name, family_version, inputs, outputs, payload_bytes):
        """
        Create transactions.
        :param family_name: string
        :param family_version: string
        :param inputs: list
        :param outputs: list
        :param payload_bytes: bytes
        """
        pass

    @staticmethod
    @abc.abstractmethod
    def send(payload):
        """
        Send transactions.
        :param payload: string
        """
        pass
