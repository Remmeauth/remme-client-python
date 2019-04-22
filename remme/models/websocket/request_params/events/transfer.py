import re

from remme.models.general.patterns import RemmePatterns


class WebSocketsTransferEventRequestParams:
    """
    Class for checking transfer event data on request parameters.
    """

    def __init__(self, data):

        self.event_type = data.get('event_type')
        self.address = data.get('address')

        if self.address is None or not isinstance(self.address, str) \
                or re.match(RemmePatterns.ADDRESS.value, self.address) is None:
            raise Exception('The `address` parameter is not correct or not provided.')

    def serialize_to_json(self):
        return {
            'event_type': self.event_type,
            'address': self.address,
        }
