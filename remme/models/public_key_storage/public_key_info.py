

class PublicKeyInfo:
    """
    Class for information about public key.
    """

    def __init__(self, data):

        self.data = data

        self.owner_public_key = self.data.get('owner_public_key')
        self.address = self.data.get('address')
        self.is_revoked = self.data.get('is_revoked')
        self.is_valid = self.data.get('is_valid')
        self.valid_from = self.data.get('valid_from')
        self.valid_to = self.data.get('valid_to')
        self.entity_hash = self.data.get('entity_hash')
        self.entity_hash_signature = self.data.get('entity_hash_signature')
        self.public_key = self.data.get('public_key')
        self.type = self.data.get('type')
