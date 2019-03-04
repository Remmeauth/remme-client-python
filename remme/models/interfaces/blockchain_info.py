import abc


class IRemmeBlockchainInfo(metaclass=abc.ABCMeta):

    @staticmethod
    @abc.abstractmethod
    def get_transactions(query=None):
        """
        Get all transactions from REMChain.

        Args:
            query (dict, optional): dictionary with specific parameters
        """
        pass

    @staticmethod
    @abc.abstractmethod
    def get_transaction_by_id(id):
        """
        Get transaction by id (header_signature) from REMChain.

        Args:
            id (string): id
        """
        pass

    @staticmethod
    @abc.abstractmethod
    def parse_transaction_payload(transaction):
        """
        Parse transaction payload. Take transaction and return object with payload and type.

        Args:
            transaction (dict): transaction payload
        """
        pass

    @staticmethod
    @abc.abstractmethod
    def get_blocks(query=None):
        """
        Get all blocks from REMChain.
        You can specify one or more query parameters.

        Args:
            query (dict, optional): dictionary with specific parameters
        """
        pass

    @staticmethod
    @abc.abstractmethod
    def get_block_by_id(id):
        """
        Get block by id (header_signature) from REMChain.

        Args:
            id (string): id
        """
        pass

    @staticmethod
    @abc.abstractmethod
    def get_block_info(query=None):
        """
        Get information about block.

        Args:
            query (dict, optional): dictionary with specific parameters
        """
        pass

    @staticmethod
    @abc.abstractmethod
    def get_batches(query=None):
        """
        Get all batches from REMChain.

        Args:
            query (dict, optional): dictionary with specific parameters
        """
        pass

    @staticmethod
    @abc.abstractmethod
    def get_batches_by_id(id):
        """
        Get batch by id (header_signature) from REMChain.

        Args:
            id (string): batch id
        """
        pass

    @staticmethod
    @abc.abstractmethod
    def get_batch_status(batch_id):
        """
        Get status of batch.

        Args:
            batch_id (string): batch id
        """
        pass

    @staticmethod
    @abc.abstractmethod
    def get_state(query=None):
        """
        Get states in REMChain.

        Args:
            query (dict, optional): dictionary with specific parameters
        """
        pass

    @staticmethod
    @abc.abstractmethod
    def get_state_by_address(address):
        """
        Get state by address.

        Args:
            address (string): address
        """
        pass

    @staticmethod
    @abc.abstractmethod
    def parse_state_data(state):
        """
        Parse state data.

        Args:
            state (dict): state data
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

    # TODO: uncomment after refactoring receipts
    # @staticmethod
    # @abc.abstractmethod
    # def get_receipts(ids):
    #     """
    #     Get transactions receipts
    #     :param ids: list of string
    #     """
    #     pass
