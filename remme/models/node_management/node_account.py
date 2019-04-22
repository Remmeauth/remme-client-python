from remme.models.node_management.bet_type import BetType
from remme.models.node_management.node_account_state import NodeAccountState

DEFAULT_NODE_ACCOUNT_INFO = {
    'node_state': NodeAccountState.NEW.value,
    'balance': '0.0000',
    'reputation': {
        'frozen': '0.0000',
        'unfrozen': '0.0000',
    },
    'last_defrost_timestamp': 0,
    'shares': [],
    'min': True,
}


class NodeAccount:
    """
    Class for information about node account.
    """

    def __init__(self, node_account_response):

        self.node_account_response = node_account_response if node_account_response else DEFAULT_NODE_ACCOUNT_INFO

        self.state = self.node_account_response.get('node_state')
        self.reputation = {
            'frozen': self.node_account_response.get('reputation').get('frozen'),
            'unfrozen': self.node_account_response.get('reputation').get('unfrozen'),
        }
        self.balance = self.node_account_response.get('balance')
        self.shares = self.node_account_response.get('shares')
        self.bet = self._get_bet_value(response=node_account_response)
        self.last_defrost_timestamp = self.node_account_response.get('last_defrost_timestamp')

    @staticmethod
    def _get_bet_value(response):

        if response.get(BetType.MIN.value.lower()):
            return {
                'type': BetType.MIN.value,
            }

        elif response.get(BetType.MAX.value.lower()):
            return {
                'type': BetType.MAX.value
            }

        elif response.get(BetType.FIXED_AMOUNT.value.lower()):
            return {
                'type': BetType.FIXED_AMOUNT.value,
                'value': response.get(BetType.FIXED_AMOUNT.value.lower()),
            }

        else:
            raise Exception('No bet set.')
