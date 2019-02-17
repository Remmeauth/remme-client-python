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
    SHA256 = r"^[a-f0-9]{64}$"
    SHA512 = r"^[a-f0-9]{128}$"
    NODE_ADDRESS = r"^(!(http|https):\/\/)?(([\w\d\-+%=~&@#?!;*,\._\(\)|$\/\\\]" \
                   r"\[-]*)(\.|\:))+([\w\d\-+%=~&@#?!;*,\._\(\)|$\/\\\]\[-]+)$"
