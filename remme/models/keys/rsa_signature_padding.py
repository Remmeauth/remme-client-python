"""
Available RSA padding for signature.
"""
from enum import Enum


class RsaSignaturePadding(Enum):

    PSS = 0
    PKCS1v15 = 1
