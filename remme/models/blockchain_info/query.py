import re

from remme.models.general.patterns import RemmePatterns


class BaseQuery:
    """
    Class for checking base query on request parameters.
    """

    def __init__(self, query):

        self.query = query

        self.head = self.query.get('head')
        self.start = self.query.get('start')
        self.family_name = self.query.get('family_name')
        self.limit = self.query.get('limit')
        self.reverse = '' if self.query.get('reverse') else 'false'

        if self.head is not None \
                and not (re.match(RemmePatterns.HEADER_SIGNATURE.value, self.head) is not None):
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
            'family_name': self.family_name,
            'limit': self.limit,
            'reverse': self.reverse,
        }


class StateQuery(BaseQuery):
    """
    Class for checking state query on request parameters.
    """

    def __init__(self, query):
        super(StateQuery, self).__init__(query)

        self.address = query.get('address')

        if isinstance(self.address, str) \
                and not (re.match(RemmePatterns.ADDRESS.value, self.address) is not None):
            raise Exception('Parameter `address` need to a valid.')

    def get(self):
        get_data = super(StateQuery, self).get()
        get_data.update({'address': self.address})
        return get_data
