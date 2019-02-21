"""
Provide enums for subscribe/unsubscribe methods.
"""
from enum import Enum


class RemmeWebSocketMethods(Enum):

    Subscribe = 'subscribe'
    Unsubscribe = 'unsubscribe'
