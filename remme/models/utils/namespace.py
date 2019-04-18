from enum import Enum


class RemmeNamespace(Enum):
    """
    First 6 symbols that belongs to family name.

    References::
        - https://sawtooth.hyperledger.org/docs/core/releases/latest/architecture/global_state.html#radix-addresses
    """

    ACCOUNT = '112007'
    NODE_ACCOUNT = '116829'
    CONSENSUS_ACCOUNT = 'fd0e4f'
    PUBLIC_KEY = 'a23be1'
    SWAP = '78173b'
