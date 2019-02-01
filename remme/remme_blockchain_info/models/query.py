import re

from remme.enums.remme_patterns import RemmePatterns


class BaseQuery:
    """
    BaseQuery.
    """

    def __init__(self, query):

        self.head = query.get('query')
        self.start = query.get('start')
        self.family_name = query.get('family_name')
        self.limit = query.get('limit')
        self.reverse = '' if query.get('reverse') else 'false'

        if self.head is not None \
                and not (re.match(RemmePatterns.HEADER_SIGNATURE.value, self.head) is not None):
            raise Exception('Parameter `head` is not a valid.')

        if self.start is not None:

            if isinstance(self.start, str) \
                    and (re.match(RemmePatterns.HEADER_SIGNATURE.value, self.start) is not None
                         or re.match(r'^[a-f0-9]{64}$', self.start) is not None) \
                    or isinstance(self.start, int):
                self.start = str(self.start)
            else:
                raise Exception('Parameter `start` is not a valid.')
