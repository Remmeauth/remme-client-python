
class TransactionService:

    _remme_rest = None
    _remme_account = None

    def __init__(self, remme_rest, remme_account):
        self._remme_account = remme_account
        self._remme_rest = remme_rest

    def create(self, settings):
        raise NotImplementedError

    def send(self, transaction):
        raise NotImplementedError

    def get_nonce(self):
        raise NotImplementedError
