
class BatchInfoDto:

    batch_id = None
    status = None
    invalid_transactions = None

    def __init__(self, batch_id, status, invalid_transactions):
        self.batch_id = batch_id
        self.status = status
        self.invalid_transactions = invalid_transactions