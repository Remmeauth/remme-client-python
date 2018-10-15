
class RemmeWebSocket:

    is_event = None
    socket_address = None
    ssl_mode = None

    def __init__(self, socket_address, ssl_mode):
        self.is_event = False
        self.socket_address = socket_address
        self.ssl_mode = ssl_mode

    def connect_to_websocket(self, callback):
        raise NotImplementedError

    def close_web_socket(self):
        raise NotImplementedError
