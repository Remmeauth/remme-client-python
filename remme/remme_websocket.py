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

    ws_connection = await transaction_result.connect_to_web_socket()
    async for msg in ws_connection.socket:
        response = BatchStateUpdateDto(**json.loads(msg.data))
        if response.type == "message" and len(response.data) > 0:
            if response.data['batch_statuses'] and 'invalid_transactions' in response.data \
                    and len(response.data['invalid_transactions']) > 0:
                raise Exception(response.data['invalid_transactions'][0])
            if response.data['batch_statuses']['status'] == BatchStatus.COMMITTED.value:
                after_balance = await remme_sender.token.get_balance(receiver_public_key_hex)
                print(f'balance is: {after_balance} REM')
                await ws_connection.close_web_socket()
    ```

    But you also can use your class for work with WebSockets. Just inherit it from RemmeWebSocket, like this:
    ```python
    class MySocketConnection(RemmeWebSocket):
         def __init__(node_address, ssl_mode, data}):
             super(MySocketConnection, self).__init__(node_address, ssl_mode)
             self.data = data


    kwargs = {"node_address":"localhost:8080", "ssl_mode":False, "data":{batch_ids: [transaction_result.batch_id,]}}}
    async with  MySocketConnection(**kwargs) as my_socket_connection:
        print("connected")
        async for msg in ws.socket:
            print(f"websocket message {msg.data}")
            response = json.loads(msg.data)
            if response['status'] == "subscribed":
                print('subscribed successfully')
                await ws.close_web_socket()

    print("connection closed")
    ```
    """

    _is_event = None
    _node_address = None
    _ssl_mode = None
    _session = None
    socket = None
    data = None

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

    async def connect_to_web_socket(self):
        """
        Method for connect to WebSocket.
        In this method implement new WebSocket instance and provided some listeners for onopen, onmessage, onclose.
        This method get callback that will be called when get events: onmessage, onclose.
        For this method you should set property data.
        ```python
        result = await transactionResult.connect_to_web_socket(call_back)
        print(result)
        my_socket_connection.close_connection()

        transactionResult.connect_to_web_socket(call_back)
        ```
        :return: {}
        """
        self._session = ClientSession()
        ws_url = self._get_subscribe_url()
        self.socket = await self._session.ws_connect(ws_url)
        result = await self.socket.send_str(self._get_socket_query())
        return self

    def _get_subscribe_url(self):
        protocol = "wss://" if self._ssl_mode else "ws://"
        events = "/events" if self._is_event else ""
        return protocol + self._node_address + '/ws' + events

    def _get_socket_query(self, is_subscribe=True):
        if not self.data:
            raise Exception("Data for subscribe was not provided")
        if self._is_event:
            query = {
                "action": "subscribe" if is_subscribe else "unsubscribe",
                "data": self.data
            }
        else:
            query = {
                "type": "request",
                "action": "subscribe" if is_subscribe else "unsubscribe",
                "entity": "batch_state",
                "id": int(time()),
                "parameters": self.data
            }
        return json.dumps(query)

    async def close_web_socket(self):
        """
        Call this method when your connection is open for close it.
        :return: None
        """
        if not self.socket:
            raise Exception("Socket is not running")
        await self.socket.send_str(self._get_socket_query(is_subscribe=False))
        await self.socket.close()
        await self._session.close()
        self.socket = None
        self._session = None

    @property
    def socket_address(self):
        """
        Get node address that was provided by user
        :return: {string}
        """
        return self._node_address

    @property
    def ssl_mode(self):
        """
        Get ssl mode that was provided by user
        :return: {string}
        """
        return self._ssl_mode

    async def __aenter__(self):
        if not self.socket:
            await self.connect_to_web_socket()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.socket:
            await self.close_web_socket()
        return False
