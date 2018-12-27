class PublicKeyInfo:
    """
    Model that return to user which want to see information about public key (public_key_storage.get_info)
    """

    def __init__(self, data):
        self.owner_public_key = data.get('owner_public_key')
        self.address = data.get('address')
        self.is_revoked = data.get('is_revoked')
        self.is_valid = data.get('is_valid')
        self.valid_from = data.get('valid_from')
        self.valid_to = data.get('valid_to')
        self.entity_hash = data.get('entity_hash')
        self.entity_hash_signature = data.get('entity_hash_signature')
        self.public_key = data.get('public_key')
        self.type = data.get('type')
