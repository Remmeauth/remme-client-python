

class TransferInfoDto:
    """
    Class for information about transfer.
    """

    def __init__(self, data):
        """
        :param data: dict {from: string, to: string}
        """
        self.data = data

        self.transfer_from = self.data.get('from')
        self.transfer_to = self.data.get('to')
