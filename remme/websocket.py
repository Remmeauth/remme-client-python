import json

from aiohttp import ClientSession

from remme.models.general.batch_status import BatchStatus
from remme.models.interfaces.websocket import IRemmeWebSocket
from remme.models.websocket.batch_info import BatchInfoDto
from remme.models.websocket.block_info import BlockInfoDto
from remme.models.websocket.events import RemmeEvents
from remme.models.websocket.json_rpc_request import JsonRpcRequest
from remme.models.websocket.methods import RemmeWebSocketMethods
from remme.models.websocket.swap_info import SwapInfo
from remme.models.websocket.transfer_info import TransferInfoDto
from remme.utils import validate_node_config


class RemmeWebSocket(IRemmeWebSocket):
    """
    Class that work with sockets. Class can be used for inheritance.
    This class is used for response on transaction sending.
    Each method that return batch_id, for truth return class that inherit from RemmeWebSocket with preset data.

    To use:
        .. code-block:: python

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

        But you also can use your class for work with WebSockets.
        Just inherit it from RemmeWebSocket, like this:

        .. code-block:: python

            class MySocketConnection(RemmeWebSocket):
                 def __init__(network_config, data):
                     super(MySocketConnection, self).__init__(network_config)
                     self.data = data

            web_socket = MySocketConnection(
                network_config={
                    "node_address":"localhost:8080",
                    "ssl_mode":False,
                },
                data={
                    "event_type":"batch",
                    "id":transaction_result.batch_id,
                }
            )
    """

    _session, _socket, data = None, None, None

    def __init__(self, network_config):
        """
        Implement RemmeWebSocket by providing node address and ssl mode.

        Args:
            network_config (dict): config of network (node address and ssl mode)

        To use:
            .. code-block:: python

                remme_web_socket = remme_events(network_config)
        """
        validate_node_config(network_config=network_config)
        self._network_config = network_config

    @property
    def network_config(self):
        """
        Return network config object which contain domain name, port and ssl.
        """
        return self._network_config

    def _map(self, event, data):

        events_data = {
            RemmeEvents.Batch.value: BatchInfoDto(data=data),
            RemmeEvents.Blocks.value: BlockInfoDto(data=data),
            RemmeEvents.AtomicSwap.value: SwapInfo(data=data),
            RemmeEvents.Transfer.value: TransferInfoDto(data=data),
        }

        return events_data.get(event)

    def _get_subscribe_url(self):
        """
        Get subscribe url.

        Returns:
            Network url in string format.
        """
        node_address, ssl_mode = self._network_config.get('node_address'), self._network_config.get('ssl_mode')
        protocol = 'wss://' if ssl_mode else 'ws://'
        return f'{protocol}{node_address}'

    def _get_socket_query(self, is_subscribe=True):
        """
        Get socket query.

        Args:
            is_subscribe (boolean): True or False

        Returns:
            Query in string format.
        """
        if not self.data:
            raise Exception('Data for subscribe was not provided.')

        method = RemmeWebSocketMethods.Subscribe.value if is_subscribe else RemmeWebSocketMethods.Unsubscribe.value

        return json.dumps(JsonRpcRequest(method=method, params=self.data).get_query())

    async def connect_to_web_socket(self):
        """
        Method for connect to WebSocket.
        For this method you should set property data.

        To use:
            .. code-block:: python

                async for msg in tx.connect_to_web_socket():
                    print('connected')
                    print('handle some messages')
                    await tx.close_web_socket()

                print('connection closed')

        Returns:
            Messages.
        """
        self._session = ClientSession()
        self._socket = await self._session.ws_connect(self._get_subscribe_url())

        await self._socket.send_str(self._get_socket_query())

        async for msg in self._socket:

            response = json.loads(msg.data)
            result, error = response.get('result'), response.get('error')

            if error:
                raise Exception(error)

            if isinstance(result, str) and result == 'SUBSCRIBED':
                yield response

            else:

                if result.get('event_type') == RemmeEvents.Batch.value \
                        and result.get('attributes').get('status') == BatchStatus.INVALID.value:
                    raise Exception(result.get('attributes'))

                yield self._map(result.get('event_type'), result.get('attributes'))

    async def close_web_socket(self):
        """
        Call this method when your connection is open for close it.
        """
        if not self._socket:
            raise Exception('WebSocket is not running.')

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
