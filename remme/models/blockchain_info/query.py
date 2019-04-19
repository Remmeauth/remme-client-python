import re

from remme.models.general.patterns import RemmePatterns
from remme.models.utils.family_name import RemmeFamilyName

FAMILY_NAMES = [
    RemmeFamilyName.ACCOUNT.value,
    RemmeFamilyName.NODE_ACCOUNT.value,
    RemmeFamilyName.PUBLIC_KEY.value,
    RemmeFamilyName.SWAP.value,
]


class BaseQuery:
    """
    Class parent for base query on request parameters.
    """

    def __init__(self, query):

        self.query = query

        self.head = self.query.get('head')
        self.start = self.query.get('start')
        self.limit = self.query.get('limit')
        self.reverse = '' if self.query.get('reverse') else 'false'

        if self.head is not None \
                and re.match(RemmePatterns.HEADER_SIGNATURE.value, self.head) is None:
            raise Exception('Parameter `head` is not a valid.')

        if self.start is not None:

            if (isinstance(self.start, str)
                    and (re.match(RemmePatterns.HEADER_SIGNATURE.value, self.start) is not None
                         or re.match(r'^0x[a-f0-9]{16}$', self.start) is not None)) \
                    or isinstance(self.start, int):
                self.start = str(self.start)
            else:
                raise Exception('Parameter `start` is not a valid.')

    def get(self):
        return {
            'head': self.head,
            'start': self.start,
            'limit': self.limit,
            'reverse': self.reverse,
        }


class FractionQuery(BaseQuery):
    """
    Class for checking block and batch query on request parameters.
    """

    def __init__(self, query):
        super(FractionQuery, self).__init__(query)

        self.ids = self.query.get('ids')

        if self.ids is not None:
            if isinstance(self.ids, list):
                for transaction_id in self.ids:

                    if not isinstance(self.ids, str) \
                            and re.match(RemmePatterns.HEADER_SIGNATURE.value, transaction_id) is None:
                        raise Exception('Parameter `ids` stris not a valid.')

            else:
                raise Exception('Parameter `ids` is not a valid.')

    def get(self):
        data = super(FractionQuery, self).get()
        data.update({'ids': self.ids})
        return data


class TransactionQuery(FractionQuery):
    """
    Class for checking transaction query on request parameters.
    """

    def __init__(self, query):
        super(TransactionQuery, self).__init__(query)

        self.family_name = self.query.get('family_name')

        if self.family_name is not None:
            if self.family_name not in FAMILY_NAMES:
                raise Exception('Parameter `family_name` is not a valid.')

    def get(self):
        data = super(TransactionQuery, self).get()
        data.update({'family_name': self.family_name})
        return data


class StateQuery(BaseQuery):
    """
    Class for checking state query on request parameters.
    """

    def __init__(self, query):
        super(StateQuery, self).__init__(query)

        self.address = query.get('address')

        if isinstance(self.address, str) \
                and re.match(RemmePatterns.ADDRESS.value, self.address) is None:
            raise Exception('Parameter `address` need to a valid.')

    def get(self):
        data = super(StateQuery, self).get()
        data.update({'address': self.address})
        return data
