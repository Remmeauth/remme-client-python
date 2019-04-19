

class NodeInfo:
    """
    Class for information about node.
    """

    def __init__(self, data):
        """
        Args:
            data (dict): is_synced (boolean), peer_count (integer)
        """
        self.data = data
        self.is_synced = self.data.get('is_synced')
        self.peer_count = self.data.get('peer_count')
