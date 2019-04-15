

class NodeConfig:
    """
    Class for information about node config.
    """

    def __init__(self, data):

        self.data = data
        self.node_public_key = data.get('node_public_key')
        self.node_address = data.get('node_address')
