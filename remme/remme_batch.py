
class RemmeBatch:

    _remme_rest = None

    def __init__(self, remme_rest):
        self._remme_rest = remme_rest

    def get_status(self, batch_id):
        raise NotImplementedError
