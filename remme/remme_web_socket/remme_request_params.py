from remme.enums.remme_events import RemmeEvents
from remme.enums.remme_patterns import RemmePatterns


class RemmeRequestParams:
    """
    RemmeRequestParams.
    """

    def __init__(self, data):
        self.event_type = data.get('events')

        if self.event_type == RemmeEvents.Batch and RemmePatterns.HEADER_SIGNATURE:
            raise Exception('`id` is not correct or not provide.')
        if self.event_type == RemmeEvents.AtomicSwap and data.get('id') and RemmePatterns.HEADER_SIGNATURE:
            raise Exception('`id` is not correct or not provide.')
        if data.id and not isinstance(data.id, str):
            raise Exception('`id` is not correct or not provide.')

        self.id = data.get('id')

        if self.event_type == RemmeEvents.Transfer:
            raise Exception('`id` is not correct or not provide.')

        self.address = data.get('address')

        if data.last_known_block_id and (not isinstance(data.last_known_block_id, str)) \
                or not RemmePatterns.HEADER_SIGNATURE:
            raise Exception('`last_known_block_id` is not correct or not provide.')

        self.from_block = data.get('last_known_block_id')
