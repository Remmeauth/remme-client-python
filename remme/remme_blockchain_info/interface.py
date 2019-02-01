import abc


class IRemmeBlockchainInfo(metaclass=abc.ABCMeta):

    @staticmethod
    @abc.abstractmethod
    def get_transactions(query=None):
        """
        Get all transactions from REMChain.
        :param query:
        """
        pass

    @staticmethod
    @abc.abstractmethod
    def get_transaction_by_id(id):
        """
        Get transaction by id (header_signature) from REMChain.
        :param id: string
        """
        pass

    @staticmethod
    @abc.abstractmethod
    def parse_transaction_payload(transaction):
        """
        Parse transaction payload. Take transaction and return object with payload and type.
        :param transaction:
        """
        pass

    @staticmethod
    @abc.abstractmethod
    def get_blocks(query=None):
        """
        Get all blocks from REMChain.
        You can specify one or more query parameters.
        :param query:
        """
        pass

    @staticmethod
    @abc.abstractmethod
    def get_block_by_id(id):
        """
        Get block by id (header_signature) from REMChain.
        :param id: string
        """
        pass

    @staticmethod
    @abc.abstractmethod
    def get_block_info(query=None):
        """
        Get information about block.
        :param query:
        """
        pass

    @staticmethod
    @abc.abstractmethod
    def get_batches(query=None):
        """
        Get all batches from REMChain.
        :param query:
        """
        pass

    @staticmethod
    @abc.abstractmethod
    def get_batches_by_id(id):
        """
        Get batch by id (header_signature) from REMChain.
        :param id: string
        """
        pass

    @staticmethod
    @abc.abstractmethod
    def get_batches_status(batch_id):
        """
        Get status of batch.
        :param batch_id: string
        """
        pass

    @staticmethod
    @abc.abstractmethod
    def get_state(query=None):
        """
        Get states in REMChain.
        :param query:
        """
        pass

    @staticmethod
    @abc.abstractmethod
    def get_state_by_address(address):
        """
        Get state by address.
        :param address: string
        """
        pass

    @staticmethod
    @abc.abstractmethod
    def parse_state_data(state):
        """
        Parse state data.
        :param state:
        """
        pass

    @staticmethod
    @abc.abstractmethod
    def get_peers():
        """
        Get peers that connected to this node.
        """
        pass

    @staticmethod
    @abc.abstractmethod
    def get_network_status():
        """
        Get network status for node.
        """
        pass
