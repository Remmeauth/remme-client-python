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

        if self.head is not None:
            if not isinstance(self.head, str) \
                    or re.match(RemmePatterns.HEADER_SIGNATURE.value, self.head) is None:

                raise Exception('Parameter `head` is not a valid.')

    def get(self):
        return {
            'head': self.head,
            'start': self.start,
            'limit': self.limit,
            'reverse': self.reverse,
        }


class BaseListQuery(BaseQuery):
    """
    Class parent for base list query on request parameters.
    """

    def __init__(self, query):
        super(BaseListQuery, self).__init__(query)

        self.ids = self.query.get('ids')

        if self.ids is not None:
            if isinstance(self.ids, list):
                for id_ in self.ids:

                    if not isinstance(id_, str) \
                            or re.match(RemmePatterns.HEADER_SIGNATURE.value, id_) is None:
                        raise Exception('Parameter `ids` is not a valid.')

            else:
                raise Exception('Parameter `ids` is not a valid.')

    def get(self):
        data = super(BaseListQuery, self).get()
        data.update({'ids': self.ids})
        return data


class BatchQuery(BaseListQuery):
    """
    Class for checking batch query on request parameters.
    """

    def __init__(self, query):
        super(BatchQuery, self).__init__(query)

        if self.start is not None:
            if not isinstance(self.start, str) \
                    or re.match(RemmePatterns.HEADER_SIGNATURE.value, self.start) is None:

                raise Exception('Parameter `start` is not a valid.')

    def get(self):
        data = super(BatchQuery, self).get()
        return data


class BlockQuery(BaseListQuery):
    """
    Class for checking block query on request parameters.
    """

    def __init__(self, query):
        super(BlockQuery, self).__init__(query)

        if self.start is not None:
            if isinstance(self.start, int):
                self.start = hex(self.start).lstrip('0x')[-16:]
                self.start = f'0x{self.start.zfill(16)}'

            if not isinstance(self.start, str) \
                    or re.match(RemmePatterns.BLOCK_NUMBER.value, self.start) is None:

                raise Exception('Parameter `start` is not a valid.')

    def get(self):
        data = super(BlockQuery, self).get()
        return data


class TransactionQuery(BaseListQuery):
    """
    Class for checking transaction query on request parameters.
    """

    def __init__(self, query):
        super(TransactionQuery, self).__init__(query)

        self.family_name = self.query.get('family_name')

        if self.family_name is not None:
            if self.family_name not in FAMILY_NAMES:
                raise Exception('Parameter `family_name` is not a valid.')

        if self.start is not None:
            if not isinstance(self.start, str) \
                    or re.match(RemmePatterns.HEADER_SIGNATURE.value, self.start) is None:

                raise Exception('Parameter `start` is not a valid.')

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

        if self.address is not None:

            if not isinstance(self.address, str) \
                    or re.match(RemmePatterns.ADDRESS.value, self.address) is None:
                raise Exception('Parameter `address` need to a valid.')

        if self.start is not None:

            if not isinstance(self.start, str) \
                    or re.match(RemmePatterns.ADDRESS.value, self.start) is None:
                raise Exception('Parameter `start` is not a valid.')

    def get(self):
        data = super(StateQuery, self).get()
        data.update({'address': self.address})
        return data
