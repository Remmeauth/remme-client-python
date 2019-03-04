

class BlockInfoDto:
    """
    Class for information about block.
    """

    def __init__(self, data):
        """
        Args:
            data (dict): id (string), timestamp (integer)
        """
        self.data = data

        self.id = self.data.get('id')
        self.timestamp = self.data.get('timestamp')
