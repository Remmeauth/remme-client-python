import abc


class IRemmePublicKeyStorage(metaclass=abc.ABCMeta):

    @staticmethod
    @abc.abstractmethod
    def create(data):
        """
        Initiation of swap.
        Send transaction into REMChain.
        :param data: dict
        """
        pass

    @staticmethod
    @abc.abstractmethod
    def store(data):
        """
        Initiation of swap.
        Send transaction into REMChain.
        :param data: dict
        """
        pass

    @staticmethod
    @abc.abstractmethod
    def create_and_store(data):
        """
        Initiation of swap.
        Send transaction into REMChain.
        :param data: dict
        """
        pass

    @staticmethod
    @abc.abstractmethod
    def check(public_key):
        """
        Initiation of swap.
        Send transaction into REMChain.
        :param public_key: string
        """
        pass

    @staticmethod
    @abc.abstractmethod
    def revoke(public_key):
        """
        Initiation of swap.
        Send transaction into REMChain.
        :param public_key: string
        """
        pass

    @staticmethod
    @abc.abstractmethod
    def get_info(public_key):
        """
        Initiation of swap.
        Send transaction into REMChain.
        :param public_key: string
        """
        pass

    @staticmethod
    @abc.abstractmethod
    def get_account_public_keys(account_public_key):
        """
        Initiation of swap.
        Send transaction into REMChain.
        :param account_public_key: string
        """
        pass
