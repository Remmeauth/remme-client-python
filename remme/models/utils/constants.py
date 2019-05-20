"""
Provide constants.
"""
from remme.models.utils.namespace import RemmeNamespace


CONSENSUS_ADDRESS = f'{RemmeNamespace.CONSENSUS_ACCOUNT.value}{"0" * 64}'
ZERO_ADDRESS = '0' * 70
BLOCK_INFO_NAMESPACE_ADDRESS = '00b10c00'
BLOCK_INFO_CONFIG_ADDRESS = '00b10c01' + '0' * 62
