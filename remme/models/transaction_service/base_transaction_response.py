import re

from remme.models.general.patterns import RemmePatterns
from remme.models.websocket.events import RemmeEvents
from remme.models.websocket.request_params.request_params import RemmeRequestParams
from remme.websocket import RemmeWebSocket


class BaseTransactionResponse(RemmeWebSocket):
    """
    Main class for response on transaction request, which contain identifier of batch and communication with WebSockets.
    """

    def __init__(self, network_config, batch_id):
        """
        Get address of node, ssl mode, and identifier of batch.
        Then implement RemmeWebSocket class and provide data to it.

        Args:
            network_config (dict): config of network (node address and ssl mode)
            batch_id (string): batch id
        """
        super(BaseTransactionResponse, self).__init__(network_config=network_config)
        self._batch_id = batch_id
        self.data = RemmeRequestParams({
            'event_type': RemmeEvents.Batch.value,
            'id': batch_id,
        })

    @property
    def batch_id(self):
        """
        Identifier of batch that contain sending transaction.
        """
        return self._batch_id

    @batch_id.setter
    async def batch_id(self, value):
        """
        Set batch id. When you provide new batch id to this object, program check web socket connection,
        if connection is open, program close it and then provide new batch id.
        And you can connect to web socket again with new batch id.

        Args:
            value (string): batch id
        """
        if re.match(RemmePatterns.HEADER_SIGNATURE.value, value) is None:
            raise Exception('Given batch id is invalid.')

        if self._socket:
            await self.close_web_socket()

        self._batch_id = value
        self.data = self.data.update({'id': value})

    async def __aenter__(self):
        return await super().__aenter__()

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await super().__aexit__(exc_type, exc_val, exc_tb)
