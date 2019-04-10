

class BlockInfo:
    """
    Class for information about block.
    """

    def __init__(self, data):

        self.data = data
        self.block_number = self.data.get('block_number')
        self.timestamp = self.data.get('timestamp')
        self.previous_header_signature = self.data.get('previous_header_signature')
        self.header_signature = self.data.get('header_signature')
        self.signer_public_key = self.data.get('signer_public_key')
        self.cert_votes = self.data.get('cert_votes')
