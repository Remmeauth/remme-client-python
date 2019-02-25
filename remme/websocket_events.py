from remme.models.interfaces.websocket_events import IRemmeWebSocketsEvents
from remme.models.websocket.request_params import RemmeRequestParams
from remme.websocket import RemmeWebSocket


class RemmeWebSocketEvents(RemmeWebSocket, IRemmeWebSocketsEvents):
    """
    Class for subscribing to events from WebSocket.

    References::
        Available types for subscribing - https://docs.remme.io/remme-core/docs/remme-ws-events.html#registered-events

    To use:
        .. code-block:: python

            from remme.models.websocket.events.RemmeEvents
            from remme.remme_websocket_events import RemmeWebSocketEvents

            remme_events = RemmeWebSocketsEvents({
                'node_address'='localhost:8080',
                'ssl_mode'=False,
            })
            remme_events.subscribe(events=RemmeEvents.AtomicSwap)
    """

    def __init__(self, network_config):
        """
        Implementation of RemmeWebSocketsEvents.

        Args:
            network_config (dict): config of network (node address and ssl mode)

        To use:
            .. code-block:: python

                remme_events = RemmeWebSocketsEvents({
                    'node_address'='localhost:8080',
                    'ssl_mode'=False,
                })
        """
        super(RemmeWebSocketEvents, self).__init__(network_config=network_config)

    async def subscribe(self, **data):
        """
        Subscribing to events from WebSocket.

        Args:
            data (kwargs): data about event

        Returns:
            Message.

        References::
            Available types for subscribing - https://docs.remme.io/remme-core/docs/remme-ws-events.html#registered-events

        To use:
            .. code-block:: python

                remme.events.subscribe(events=RemmeEvents.AtomicSwap.value)
        """
        if self._socket:
            await self.close_web_socket()

        self.data = RemmeRequestParams(data=data).get_data()

        return self.connect_to_web_socket()

    async def unsubscribe(self, **data):
        """
        Unsubscribing from events.
        Regardless of how many events you subscribed to, you always unsubscribe from all.

        To use:
            .. code-block:: python

                remme_events.unsubscribe()
        """
        self.data = data

        await self.close_web_socket()
