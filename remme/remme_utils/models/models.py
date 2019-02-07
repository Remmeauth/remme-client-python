from enum import Enum


class RemmeNamespace(Enum):
    """
    First 6 symbols that belongs to family name.

    References:
        - https://sawtooth.hyperledger.org/docs/core/releases/latest/architecture/global_state.html#radix-addresses
    """

    ACCOUNT = '112007'
    PUBLIC_KEY = 'a23be1'
    SWAP = '78173b'


class RemmeFamilyName(Enum):
    """
    All family names that defined into remChain.
    """

    ACCOUNT = 'account'
    PUBLIC_KEY = 'pub_key'
    SWAP = 'AtomicSwap'
