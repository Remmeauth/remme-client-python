import re

from remme.models.general.patterns import RemmePatterns


class WebSocketsAtomicSwapEventRequestParams:
    """
    Class for checking Atomic Swap event data on request parameters.
    """

    def __init__(self, data):

        self.event_type = data.get('event_type')
        self.id = data.get('id')
        self.from_block = data.get('last_known_block_id')

        if self.id is not None:

            if not isinstance(self.id, str) \
                    or re.match(RemmePatterns.SWAP_ID.value, self.id) is None:
                raise Exception('The `id` parameter is not correct.')

        if self.from_block is not None:

            if not isinstance(self.from_block, str) \
                    or re.match(RemmePatterns.HEADER_SIGNATURE.value, self.from_block) is None:
                raise Exception('The `last_known_block_id` parameter is not correct.')

    def serialize_to_json(self):

        params = {'event_type': self.event_type}

        if self.id is not None:
            params['id'] = self.id

        if self.from_block is not None:
            params['from_block'] = self.from_block

        return params
