"""
Provide enums for Remme patterns.
"""
from enum import Enum


class RemmePatterns(Enum):

    PRIVATE_KEY = r"^[a-f0-9]{64}$"
    PUBLIC_KEY = r"^[a-f0-9]{66}$"
    ADDRESS = r"^[a-f0-9]{70}$"
    SWAP_ID = r"^[a-f0-9]{64}$"
    HEADER_SIGNATURE = r"^[a-f0-9]{128}$"
    BLOCK_NUMBER = r"^0x[a-f0-9]{16}$"
    SHA256 = r"^[a-f0-9]{64}$"
    SHA512 = r"^[a-f0-9]{128}$"
    PROTOCOL = r"^(?!(http|https|ws|wss):\/\/)\S+$"
