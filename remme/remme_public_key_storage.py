
class RemmePublicKeyStorage:

    _remme_api = None
    _remme_transaction = None
    _remme_account = None

    def __init__(self, remme_api, remme_transaction, remme_account):
        self._remme_api = remme_api
        self._remme_transaction = remme_transaction
        self._remme_account = remme_account

    def store(self, _a):
        raise NotImplementedError

    def check(self, public_key):
        raise NotImplementedError

    def revoke(self, public_key):
        raise NotImplementedError

    def get_user_public_key(self, user_account_public_key):
        raise NotImplementedError

    def generate_message(self, data):
        raise NotImplementedError

    def generate_entity_hash(self, message):
        raise NotImplementedError
