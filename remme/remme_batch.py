import re
from remme.remme_methods import RemmeMethods


class RemmeBatch:

    _remme_api = None

    def __init__(self, remme_api):
        self._remme_api = remme_api

    @staticmethod
    def is_valid_batch_id(_batch_id):
        return re.match(r"^[0-9a-f]{128}$", _batch_id) is not None

    async def get_status(self, batch_id):
        if not self.is_valid_batch_id(batch_id):
            raise Exception("Invalid batch id given.")
        params = {'id': batch_id}
        return await self._remme_api.send_request(RemmeMethods.BATCH_STATUS, params)
