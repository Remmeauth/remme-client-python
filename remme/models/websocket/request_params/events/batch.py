import re

from remme.models.general.patterns import RemmePatterns


class WebSocketsBatchEventRequestParams:
    """
    Class for checking batch event data on request parameters.
    """

    def __init__(self, data):

        self.event_type = data.get('event_type')
        self.id = data.get('id')

        if self.id is None or not isinstance(self.id, str) \
                or re.match(RemmePatterns.HEADER_SIGNATURE.value, self.id) is None:
            raise Exception('The `id` parameter is not correct or not provided.')

    def serialize_to_json(self):
        return {
            'event_type': self.event_type,
            'id': self.id,
        }
