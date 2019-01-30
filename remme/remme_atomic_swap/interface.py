import abc


class IRemmeSwap(metaclass=abc.ABCMeta):

    @staticmethod
    @abc.abstractmethod
    def init(data):
        """

        :param data: dict
        :return:
        """
        pass

    @staticmethod
    @abc.abstractmethod
    def approve(swap_id):
        """

        :param swap_id: string
        :return:
        """
        pass

    @staticmethod
    @abc.abstractmethod
    def expire(swap_id):
        """

        :param swap_id: string
        :return:
        """
        pass

    @staticmethod
    @abc.abstractmethod
    def set_secret_lock(swap_id, secret_lock):
        """

        :param swap_id: string
        :param secret_lock: string
        :return:
        """
        pass

    @staticmethod
    @abc.abstractmethod
    def close(swap_id, secret_key):
        """

        :param swap_id: string
        :param secret_key: string
        :return:
        """
        pass

    @staticmethod
    @abc.abstractmethod
    def get_info(swap_id):
        """

        :param swap_id: string
        :return:
        """
        pass

    @staticmethod
    @abc.abstractmethod
    def get_public_key():
        """

        :return:
        """
        pass
