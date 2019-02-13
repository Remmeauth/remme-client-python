import json

from aiohttp import ClientSession

from remme.interfaces.websocket import IRemmeWebSocket
from remme.models.general.batch_status import BatchStatus
from remme.models.websocket.events import RemmeEvents
from remme.models.websocket.json_rpc_request import JsonRpcRequest
from remme.models.websocket.methods import RemmeWebSocketMethods


class RemmeWebSocket(IRemmeWebSocket):
    """
    Class that work with sockets. Class can be used for inheritance.
    This class is used for response on transaction sending.
    Each method that return batch_id, for truth return class that inherit from RemmeWebSocket with preset data.
    So for example:
    @example
    ```python
    remme = Remme()
    some_remme_address = "03c2e53acce583c8bb2382319f4dee3e816b67f3a733ef90fe3329062251d0c638"
    transaction_result = await remme.token.transfer(some_remme_address, 10)

    # transaction_result is inherit from RemmeWebSocket and
    #    self.data = {
    #        "event_type": "batch",
    #        "id": transaction_result.batch_id,
    #    }
    # so you can connect_to_web_socket easy. Just:

    async for msg in transaction_result.connect_to_web_socket():
        print(msg)
        await transaction_result.close_web_socket()
    ```

    But you also can use your class for work with WebSockets. Just inherit it from RemmeWebSocket, like this:
    ```python
    class MySocketConnection(RemmeWebSocket):
         def __init__(node_address, ssl_mode, data):
             super(MySocketConnection, self).__init__(node_address, ssl_mode)
             self.data = data

    web_socket = MySocketConnection(
        network_config={
            "node_address":"localhost:8080",
            "ssl_mode":False
        },
        data={
            "event_type":"batch",
            "id":transaction_result.batch_id
        }
    )
    ```
    """

    _session, _socket, data = None, None, None

    def __init__(self, node_address, ssl_mode):
        """
        Implement RemmeWebSocket by providing node address and ssl mode.
        @example
        ```python
        remme_web_socket = remme_events(node_address, ssl_mode)
        ```
        :param node_address: string
        :param ssl_mode: boolean
        """
        self._node_address = node_address
        self._ssl_mode = ssl_mode

    def _get_subscribe_url(self):
        """
        Get subscribe url.
        :return: network url in string format
        """
        protocol = "wss://" if self._ssl_mode else "ws://"
        return protocol + self._node_address

    def _get_socket_query(self, is_subscribe=True):
        """
        Get socket query.
        :param is_subscribe: boolean
        :return: query in string format
        """
        if not self.data:
            raise Exception("Data for subscribe was not provided.")

        method = RemmeWebSocketMethods.Subscribe.value if is_subscribe else RemmeWebSocketMethods.Unsubscribe.value

        return json.dumps(JsonRpcRequest(method=method, params=self.data).get_query())

    async def connect_to_web_socket(self):
        """
        Method for connect to WebSocket.
        For this method you should set property data.
        ```python
        async for msg in tx.connect_to_web_socket():
            print("connected")
            print("handle some messages")
            await tx.close_web_socket()

        print("connection closed")
        ```
        :return: async messages
        """
        self._session = ClientSession()
        self._socket = await self._session.ws_connect(self._get_subscribe_url())

        await self._socket.send_str(self._get_socket_query())

        async for msg in self._socket:

            response = json.loads(msg.data)
            result, error = response.get('result'), response.get('error')

            if error:
                raise Exception(error)

            if not isinstance(result, str):
                if result.get('event_type') == RemmeEvents.Batch.value \
                        and result.get('attributes').get('status') == BatchStatus.INVALID.value:
                    raise Exception(result.get('attributes'))

            yield response

    async def close_web_socket(self):
        """
        Call this method when your connection is open for close it.
        """
        if not self._socket:
            raise Exception("WebSocket is not running.")

        await self._socket.send_str(self._get_socket_query(is_subscribe=False))

        await self._socket.close()
        await self._session.close()
        self._socket, self._session = None, None

    async def __aenter__(self):
        if not self._socket:
            yield self.connect_to_web_socket()
        yield self._socket

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self._socket:
            await self.close_web_socket()
        return False
