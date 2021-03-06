"""
Enumeration all currently available methods in our JSON-RPC.
"""
from enum import Enum


class RemmeMethods(Enum):

    PUBLIC_KEY = 'get_public_key_info'
    TOKEN = 'get_balance'
    BATCH_STATUS = 'get_batch_status'
    ATOMIC_SWAP = 'get_atomic_swap_info'
    ATOMIC_SWAP_PUBLIC_KEY = 'get_atomic_swap_public_key'
    USER_PUBLIC_KEY = 'get_public_keys_list'
    NODE_KEY = 'get_node_public_key'
    NODE_CONFIG = 'get_node_config'
    NODE_PRIVATE_KEY = 'export_node_key'
    TRANSACTION = 'send_raw_transaction'
    NETWORK_STATUS = 'get_node_info'
    BLOCK_INFO = 'get_blocks'
    BLOCKS = 'list_blocks'
    FETCH_BLOCK = 'fetch_block'
    BATCHES = 'list_batches'
    FETCH_BATCH = 'fetch_batch'
    TRANSACTIONS = 'list_transactions'
    FETCH_TRANSACTION = 'fetch_transaction'
    STATE = 'list_state'
    FETCH_STATE = 'fetch_state'
    PEERS = 'fetch_peers'
    RECEIPTS = 'list_receipts'
    NODE_ACCOUNT = 'get_node_account'
