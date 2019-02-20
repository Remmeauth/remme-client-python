

class SwapInfo:
    """
    Class DTO for swap information.
    """

    def __init__(self, data):

        self.data = data

        self.state = self.data.get('state')
        self.receiver_address = self.data.get('receiver_address')
        self.amount = self.data.get('amount')
        self.email = self.data.get('email_address_encrypted_optional')
        self.secret_lock = self.data.get('secret_lock')
        self.secret_key = self.data.get('secret_key')
        self.created_at = self.data.get('created_at')
        self.is_initiator = self.data.get('is_initiator')
        self.sender_address = self.data.get('sender_address')
        self.sender_address_non_local = self.data.get('sender_address_non_local')
        self.swap_id = self.data.get('swap_id')
