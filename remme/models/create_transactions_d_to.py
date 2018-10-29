
class CreateTransactionDto:
    family_name = None
    family_version = None
    inputs = None
    outputs = None
    payload_bytes = None

    def __init__(self, family_name, family_version, inputs, outputs, payload_bytes):
        self.family_name = family_name
        self.family_version = family_version
        self.inputs = inputs
        self.outputs = outputs
        self.payload_bytes = payload_bytes