

class NetworkStatus:
    """
    NetworkStatus.
    """

    def __init__(self, network_status):
        """
        :param network_status: {is_synced: boolean, peer_count: integer}
        """

        self.is_synced = network_status.get('is_synced')
        self.peer_count = network_status.get('peer_count')
