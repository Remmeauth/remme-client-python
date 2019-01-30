"""
Provide enums for Remme events.
"""
from enum import Enum


class RemmeEvents(Enum):

    Blocks = 'blocks'
    Batch = 'batch'
    Transfer = 'transfer'
    AtomicSwap = 'atomic_swap'
