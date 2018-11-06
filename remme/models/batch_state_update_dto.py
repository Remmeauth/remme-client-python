
class BatchStateUpdateDto:

    id = None
    type = None
    data = None
    status = None

    def __init__(self, id, type, data=None, status=None):
        self.id = id
        self.type = type
        self.data = data
        self.status = status