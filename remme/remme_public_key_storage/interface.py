import abc


class IRemmePublicKeyStorage(metaclass=abc.ABCMeta):

    @staticmethod
    @abc.abstractmethod
    def create(data):
        """
        Create public key payload in bytes to store with another payer, private_key and public_key.
        :param data: dict
        """
        pass

    @staticmethod
    @abc.abstractmethod
    def store(data):
        """
        Store public key payload bytes with data into REMChain.
        Send transaction to chain.
        :param data: bytes
        """
        pass

    @staticmethod
    @abc.abstractmethod
    def create_and_store(data):
        """
        Create public key payload bytes and store public key with its data into REMChain.
        Send transaction to chain with private key.
        :param data: dict
        """
        pass

    @staticmethod
    @abc.abstractmethod
    def check(public_key):
        """
        Check public key on validity and revocation.
        Take address of public key.
        :param public_key: string
        """
        pass

    @staticmethod
    @abc.abstractmethod
    def revoke(public_key):
        """
        Revoke public key by address.
        Take address of public key. Send transaction to chain.
        :param public_key: string
        """
        pass

    @staticmethod
    @abc.abstractmethod
    def get_info(public_key):
        """
        Get info about this public key.
        Take address of public key.
        :param public_key: string
        """
        pass

    @staticmethod
    @abc.abstractmethod
    def get_account_public_keys(account_public_key):
        """
        Take account address (which describe in RemmePatterns.ADDRESS).
        :param account_public_key: string
        """
        pass
