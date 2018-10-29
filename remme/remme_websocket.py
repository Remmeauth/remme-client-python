from aiohttp import ClientSession, WSMsgType
from time import time
import json


class RemmeWebSocket:

    _is_event = None
    _socket_address = None
    _ssl_mode = None
    _data = None
    _socket = None

    def __init__(self, socket_address, ssl_mode):
        self._is_event = False
        self._socket_address = socket_address
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
        return protocol + self._socket_address + '/ws' + events

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

    def get_socket_address(self):
        return self._socket_address

    def get_ssl_mode(self):
        return self._ssl_mode
