

class BatchInfoDto:
    """
    Class for information about batch.
    """

    def __init__(self, data):
        """
        :param data: dict {status: string, id: string}
        """
        self.data = data

        self.status = self.data.get('status')
        self.batch_id = self.data.get('id')
