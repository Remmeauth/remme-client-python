
class CreateTransactionDto:
    """
    Wrapper class for creating transaction before send,
    which contain family name, family version, inputs, outputs, serialized data.
    """
    family_name = None
    family_version = None
    inputs = None
    outputs = None
    payload_bytes = None

    def __init__(self, family_name, family_version, inputs, outputs, payload_bytes):
        """
        Documentation for building transactions
        https://sawtooth.hyperledger.org/docs/core/releases/latest/_autogen/sdk_submit_tutorial_python.html#building-the-transaction
        :param family_name: {string}
        :param family_version: {string}
        :param inputs: {list}
        :param outputs: {list}
        :param payload_bytes: {bytes}
        """
        self.family_name = family_name
        self.family_version = family_version
        self.inputs = inputs
        self.outputs = outputs
        self.payload_bytes = payload_bytes