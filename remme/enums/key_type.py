"""
Provide enums for Remme key types.
"""
from enum import Enum


class KeyType(Enum):

    RSA = 0
    ECDSA = 1
    EdDSA = 2
