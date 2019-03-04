import abc


class IRemmeWebSocket(metaclass=abc.ABCMeta):

    @staticmethod
    @abc.abstractmethod
    def connect_to_web_socket():
        """
        Method for connect to WebSocket.
        For this method you should set property data.
        """
        pass

    @staticmethod
    @abc.abstractmethod
    def close_web_socket():
        """
        Call this method when your connection is open for close it.
        """
        pass
