import abc


class IRemmeWebSocketsEvents(metaclass=abc.ABCMeta):

    @staticmethod
    @abc.abstractmethod
    def subscribe(data):
        """
        Subscribing to events from WebSocket.

        Args:
            data (kwargs): data about event
        """
        pass

    @staticmethod
    @abc.abstractmethod
    def unsubscribe():
        """
        Unsubscribing from events.
        Regardless of how many events you subscribed to, you always unsubscribe from all.
        """
        pass
