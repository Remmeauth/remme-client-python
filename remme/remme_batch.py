import re


class RemmeBatch:

    _remme_rest = None

    def __init__(self, remme_rest):
        self._remme_rest = remme_rest

    @staticmethod
    def is_valid_batch_id(_batch_id):
        return re.match(r"^[0-9a-f]{128}$", _batch_id) is not None

    async def get_status(self, batch_id):
        if not self.is_valid_batch_id(batch_id):
            raise Exception("Invalid batch id given.")
        route = f"/api/v1/batch_status/{batch_id}"
        result = await self._remme_rest.get(route)
        if result['status'] == "OK":
            data = result['data']
            return data['status']
        raise Exception("Failed to get batch status")
