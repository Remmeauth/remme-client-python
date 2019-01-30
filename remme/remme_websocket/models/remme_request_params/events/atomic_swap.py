import re

from remme.enums.remme_patterns import RemmePatterns


class WebSocketsAtomicSwapEventRequestParams:
    """
    Class for checking Atomic Swap event data on request parameters.
    """

    def __init__(self, data):

        self.event_type = data.get('event_type')
        self.id = data.get('id')
        self.from_block = data.get('last_known_block_id')

        if self.id is None or not (re.match(RemmePatterns.SWAP_ID.value, self.id) is not None) \
                or not isinstance(self.id, str):
            raise Exception('The `id` parameter is not correct or not provided.')

        if self.from_block is None or not isinstance(self.from_block, str) \
                or not (re.match(RemmePatterns.HEADER_SIGNATURE.value, self.from_block) is not None):
            raise Exception('The `last_known_block_id` parameter is not correct or not provided.')

    def serialize_to_json(self):

        params = {'event_type': self.event_type}

        if self.id is not None:
            params['id'] = self.id

        if self.from_block is not None:
            params['from_block'] = self.from_block

        return params
