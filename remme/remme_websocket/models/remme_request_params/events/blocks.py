

class WebSocketsBlocksEventRequestParams:
    """
    Class for checking blocks event data on request parameters.
    """

    def __init__(self, data):
        self.event_type = data.get('event_type')

    def serialize_to_json(self):
        return {
            'event_type': self.event_type,
        }
