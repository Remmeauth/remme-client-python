import abc


class IRemmeSwap(metaclass=abc.ABCMeta):

    @staticmethod
    @abc.abstractmethod
    def init(data):
        """
        Initiation of swap.
        Send transaction into REMChain.
        :param data: dict
        """
        pass

    @staticmethod
    @abc.abstractmethod
    def approve(swap_id):
        """
        Approve swap with given id.
        Send transaction into REMChain.
        :param swap_id: string
        """
        pass

    @staticmethod
    @abc.abstractmethod
    def expire(swap_id):
        """
        Expire swap with given id. Could be expired after 24h after initiation.
        Send transaction into REMChain.
        :param swap_id: string
        """
        pass

    @staticmethod
    @abc.abstractmethod
    def set_secret_lock(swap_id, secret_lock):
        """
        Set secret lock to swap with given swap id.
        Send transaction into REMChain.
        :param swap_id: string
        :param secret_lock: string
        """
        pass

    @staticmethod
    @abc.abstractmethod
    def close(swap_id, secret_key):
        """
        Close swap with given id and secret key for checking who can close swap.
        Send transaction into REMChain.
        :param swap_id: string
        :param secret_key: string
        """
        pass

    @staticmethod
    @abc.abstractmethod
    def get_info(swap_id):
        """
        Get info about swap by given swap id.
        :param swap_id: string
        """
        pass

    @staticmethod
    @abc.abstractmethod
    def get_public_key():
        """
        Get swap public key.
        """
        pass
