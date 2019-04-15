"""
Provide enums for Bet types.
"""
from enum import Enum


class BetType(Enum):

    MIN = 'MIN'
    MAX = 'MAX'
    FIXED_AMOUNT = 'FIXED_AMOUNT'
