

class NodeInfo:
    """
    Class for information about node.
    """

    def __init__(self, node_info):
        """
        Args:
            node_info (dict): is_synced (boolean), peer_count (integer)
        """
        self.node_info = node_info

        self.is_synced = self.node_info.get('is_synced')
        self.peer_count = self.node_info.get('peer_count')
