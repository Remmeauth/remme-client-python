import abc


class IRemmeWebSocketsEvents(metaclass=abc.ABCMeta):

    @staticmethod
    @abc.abstractmethod
    def subscribe(data):
        """
        Subscribing to events from WebSocket.
        :param data: dict
        """
        pass

    @staticmethod
    @abc.abstractmethod
    def unsubscribe():
        """
        Unsubscribing from events.
        """
        pass
