from remme.remme_websocket import RemmeWebSocket
from remme.remme_websocket_events.interface import IRemmeWebSocketsEvents
from remme.remme_websocket_events.remme_request_params import RemmeRequestParams


class RemmeWebSocketEvents(RemmeWebSocket, IRemmeWebSocketsEvents):
    """
    Class for subscribing to events from WebSocket.
    Available types for subscribing is covered in
    https://docs.remme.io/remme-core/docs/remme-ws-events.html#registered-events
    @example
    ```python
    from remme.enums.remme_events import RemmeEvents
    from remme.remme_websocket_events import RemmeWebSocketEvents
    remme_events = RemmeWebSocketsEvents(
        node_address='localhost:8080',
        ssl_mode=False,
    )
    remme_events.subscribe(events=RemmeEvents.AtomicSwap)
    ```
    """

    def __init__(self, node_address, ssl_mode):
        """
        Implementation of RemmeWebSocketsEvents.
        ```python
        remme_events = RemmeWebSocketsEvents(
            node_address='localhost:8080',
            ssl_mode=False,
        )
        ```
        :param node_address: string
        :param ssl_mode: boolean
        """
        super(RemmeWebSocketEvents, self).__init__(node_address=node_address, ssl_mode=ssl_mode)

    async def subscribe(self, **data):
        """
        Subscribing to events from WebSocket.
        Available types for subscribing is covered in
        https://docs.remme.io/remme-core/docs/remme-ws-events.html#registered-events
        ```python
        remme_events.subscribe(events=RemmeEvents.AtomicSwap.value)
        ```
        :param data: dict
        """
        if self._socket:
            await self.close_web_socket()

        self.data = RemmeRequestParams(data=data).get_data()

        return self.connect_to_web_socket()

    async def unsubscribe(self, **data):
        """
        Unsubscribing from events.
        Regardless of how many events you subscribed to, you always unsubscribe from all.
        ```python
        remme_events.unsubscribe()
        ```
        """
        self.data = data

        await self.close_web_socket()
