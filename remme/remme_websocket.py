
class RemmeWebSocket:

    _is_event = None
    _socket_address = None
    _ssl_mode = None
    _data = None

    def __init__(self, socket_address, ssl_mode):
        self._is_event = False
        self._socket_address = socket_address
        self._ssl_mode = ssl_mode

    def connect_to_websocket(self, callback):
        raise NotImplementedError

    def close_websocket(self):
        raise NotImplementedError

    def get_socket_address(self):
        return self._socket_address

    def get_ssl_mode(self):
        return self._ssl_mode
