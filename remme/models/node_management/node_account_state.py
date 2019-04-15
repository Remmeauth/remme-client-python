"""
Provide enums for Node account states.
"""
from enum import Enum


class NodeAccountState(Enum):

    NEW = 'NEW'
    CLOSED = 'CLOSED'
    OPENED = 'OPENED'
