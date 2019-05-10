import re

from remme.models.general.patterns import RemmePatterns


class SwapInitDto:
    """
    Class for checking swap data on request parameters.
    """

    def __init__(self, data):

        self.data = data

        if self.data == {}:
            raise Exception('The swap data is not specified.')

        self.receiver_address = self.data.get('receiver_address')
        self.sender_address_non_local = self.data.get('sender_address_non_local')
        self.amount = self.data.get('amount')
        self.swap_id = self.data.get('swap_id')
        self.secret_lock_by_solicitor = self.data.get('secret_lock_by_solicitor')
        self.email_address_encrypted_by_initiator = self.data.get('email_address_encrypted_by_initiator')

        if self.receiver_address is None \
                or re.match(RemmePatterns.ADDRESS.value, self.receiver_address) is None:
            raise Exception('The `receiver_address` is not a valid or not specified.')

        if self.sender_address_non_local is None:
            raise Exception('The `sender_address_non_local` is not specified.')

        if self.amount is None:
            raise Exception('The `amount` is not specified.')

        if self.swap_id is None \
                or re.match(RemmePatterns.SWAP_ID.value, self.swap_id) is None:
            raise Exception('The `swap_id` is not a valid or not specified.')

        if self.secret_lock_by_solicitor \
                and re.match(RemmePatterns.PRIVATE_KEY.value, self.secret_lock_by_solicitor) is None:
            raise Exception('The `secret_lock_by_solicitor` is not a valid.')
