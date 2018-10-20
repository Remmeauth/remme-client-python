
class RemmeCertificate:

    _rsa_key_size = None
    _remme_public_key_storage = None

    def __init__(self, remme_public_key_storage):
        self._rsa_key_size = 2048
        self._remme_public_key_storage = remme_public_key_storage

    async def create_and_store(self, certificate_data_to_create):
        raise NotImplementedError

    def store(self, certificate):
        raise NotImplementedError

    def check(self, certificate):
        raise NotImplementedError

    def revoke(self, certificate):
        raise NotImplementedError