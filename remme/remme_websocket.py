from aiohttp import ClientSession, WSMsgType
from time import time
import json


class RemmeWebSocket:
    """
    Class that work with sockets. Class can be used for inheritance.
    This class is used for response on transaction sending.
    Each method that return batch_id, for truth return class that inherit from RemmeWebSocket with preset data.
    So for example:
    @example
    ```python
    remme = new Remme()
    some_remme_address = "03c2e53acce583c8bb2382319f4dee3e816b67f3a733ef90fe3329062251d0c638"
    transaction_result = await remme.token.transfer(some_remme_address, 10)

    # transaction_result is inherit from RemmeWebSocket and self.data = {
    #        batch_ids: [
    #           transactionResult.batchId,
    #        ],
    #    }
    # so you can connect_to_web_socket easy. Just:

    def callback(err, res):
        if err:
            print(err)
            return
        print(res)
        my_socket_connection.close_connection()

    transactionResult.connect_to_web_socket(callback)
    ```

    But you also can use your class for work with WebSockets. Just inherit it from RemmeWebSocket, like this:
    ```python
    class MySocketConnection(RemmeWebSocket) {
         def __init__({node_address: node_address, ssl_mode: ssl_mode, data: data}) {
             super(node_address, ssl_mode)
             self.data = data
         }
    }

    my_socket_connection = MySocketConnection({
         node_address: "localhost:8080",
         ssl_mode: False,
         data: {
             batch_ids: [
                transaction_result.batch_id,
             ],
         }
    })

    def callback(err, res):
        if err:
            print(err)
            return
        print(res)
        my_socket_connection.close_connection()

    my_socket_connection.connect_to_web_socket(callback)
    ```
    """

    _is_event = None
    _node_address = None
    _ssl_mode = None
    _data = None
    _socket = None

    def __init__(self, node_address, ssl_mode):
        """
        Implement RemmeWebSocket by providing node address and ssl mode.
        @example
        ```python
        remme_web_socket = RemmeWebSocket(node_address, ssl_mode)
        ```
        :param node_address: {string}
        :param ssl_mode: {boolean}
        """
        self._is_event = False
        self._node_address = node_address
        self._ssl_mode = ssl_mode

    async def connect_to_websocket(self, callback):
        session = ClientSession()
        self._socket = await session.ws_connect(self._get_subscribe_url())
        async for msg in self._socket:
            if msg.type == WSMsgType.TEXT:
                print(msg)
            elif msg.type == WSMsgType.ERROR:
                print(msg)

    def _get_subscribe_url(self):
        protocol = "wss://" if self._ssl_mode else "ws://"
        events = "/events" if self._is_event else ""
        return protocol + self._node_address + '/ws' + events

    def _get_socket_query(self, is_subscribe=True):
        if not self._data:
            raise Exception("Data for subscribe was not provided")
        if self._is_event:
            query = {
                "action": "subscribe" if is_subscribe else "unsubscribe",
                "data": self._data
            }
        else:
            query = {
                "type": "request",
                "action": "subscribe" if is_subscribe else "unsubscribe",
                "entity": "batch_state",
                "id": int(time()),
                "parameters": self._data
            }
        return json.dumps(query)

    def close_websocket(self):
        if not self._socket:
            raise Exception("Socket is not running")
        if self._socket.ready_state == 1:
            self._socket.send(self._get_socket_query(is_subscribe=False))
        self._socket.close()
        self._socket = None

    @property
    def socket_address(self):
        return self._node_address

    @property
    def ssl_mode(self):
        return self._ssl_mode
