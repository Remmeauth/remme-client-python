from remme.models.websocket.events import RemmeEvents
from remme.models.websocket.request_params.events.atomic_swap import WebSocketsAtomicSwapEventRequestParams
from remme.models.websocket.request_params.events.batch import WebSocketsBatchEventRequestParams
from remme.models.websocket.request_params.events.blocks import WebSocketsBlocksEventRequestParams
from remme.models.websocket.request_params.events.transfer import WebSocketsTransferEventRequestParams

SUPPORTED_NODE_EVENTS = [
    RemmeEvents.AtomicSwap.value,
    RemmeEvents.Batch.value,
    RemmeEvents.Blocks.value,
    RemmeEvents.Transfer.value,
]


class RemmeRequestParams:
    """
    Class for checking data on request parameters.
    """

    def __init__(self, data):
        self.data = data
        self.event_type = self.data.get('event_type')

    def get_data(self):

        if self.event_type not in SUPPORTED_NODE_EVENTS:
            raise Exception('Specified event type is not supported.')

        if self.event_type == RemmeEvents.Blocks.value:
            return WebSocketsBlocksEventRequestParams(data=self.data).serialize_to_json()

        if self.event_type == RemmeEvents.Batch.value:
            return WebSocketsBatchEventRequestParams(data=self.data).serialize_to_json()

        if self.event_type == RemmeEvents.Transfer.value:
            return WebSocketsTransferEventRequestParams(data=self.data).serialize_to_json()

        if self.event_type == RemmeEvents.AtomicSwap.value:
            return WebSocketsAtomicSwapEventRequestParams(data=self.data).serialize_to_json()
