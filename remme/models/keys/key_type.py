"""
Provide enums for Remme key types.
"""
from enum import Enum


class KeyType(Enum):

    RSA = 'rsa'
    ECDSA = 'ecdsa'
    EdDSA = 'ed25519'
