

class NetworkStatus:
    """
    Class for information about network status.
    """

    def __init__(self, network_status):
        """
        Args:
            network_status (dict): is_synced (boolean), peer_count (integer)
        """
        self.network_status = network_status

        self.is_synced = self.network_status.get('is_synced')
        self.peer_count = self.network_status.get('peer_count')
