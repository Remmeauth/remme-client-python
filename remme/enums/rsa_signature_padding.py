"""
Available RSA padding for signature.
"""
from enum import Enum, auto


class RsaSignaturePadding(Enum):

    EMPTY = auto()
    PSS = auto()
    PKCS1v15 = auto()
