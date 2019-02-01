

class BlockInfo:
    """
    BlockInfo.
    """

    def __init__(self, data):

        self.block_number = data.get('block_number')
        self.timestamp = data.get('timestamp')
        self.previous_header_signature = data.get('previous_header_signature')
        self.header_signature = data.get('header_signature')
        self.signer_public_key = data.get('signer_public_key')
