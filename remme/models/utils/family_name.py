"""
Provide enums for Remme family names.
"""
from enum import Enum


class RemmeFamilyName(Enum):
    """
    All family names that defined into remChain.
    """

    ACCOUNT = 'account'
    NODE_ACCOUNT = 'node_account'
    CONSENSUS_ACCOUNT = 'consensus_account'
    PUBLIC_KEY = 'pub_key'
    SWAP = 'AtomicSwap'
