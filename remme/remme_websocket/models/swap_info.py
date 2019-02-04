

class SwapInfo:
    """
    Class DTO for swap information.
    """

    def __init__(self, data):

        self.state = data.get('state')
        self.receiver_address = data.get('receiver_address')
        self.amount = data.get('amount')
        self.email = data.get('email_address_encrypted_optional')
        self.secret_lock = data.get('secret_lock')
        self.secret_key = data.get('secret_key')
        self.created_at = data.get('created_at')
        self.is_initiator = data.get('is_initiator')
        self.sender_address = data.get('sender_address')
        self.sender_address_non_local = data.get('sender_address_non_local')
        self.swap_id = data.get('swap_id')
