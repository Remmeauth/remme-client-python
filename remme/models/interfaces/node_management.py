import abc


class IRemmeNodeManagement(metaclass=abc.ABCMeta):

    @staticmethod
    @abc.abstractmethod
    def open_node():
        """
        Open node.

        To use:
            .. code-block:: python

                open_node = await remme.node_management.open_node()
        """
        pass

    @staticmethod
    @abc.abstractmethod
    def open_master_node(amount):
        """
        Open master node by amount.

        Args:
            amount (integer): amount of stake.

        To use:
            .. code-block:: python

                open_master_node = await remme.node_management.open_master_node(amount=250001)
        """
        pass

    @staticmethod
    @abc.abstractmethod
    def close_master_node():
        """
        Close master node.

        To use:
            .. code-block:: python

                close_master_node = await remme.node_management.close_master_node()
        """
        pass

    @staticmethod
    @abc.abstractmethod
    def set_bet(bet_type):
        """
        Set bet by payload (fixed_amount, max, min).

        Args:
            bet_type (string or integer): fixed_amount, max, min

        To use:
            .. code-block:: python

                set_bet = await remme.node_management.set_bet({'fixed_amount':1})
        """
        pass

    @staticmethod
    @abc.abstractmethod
    def get_initial_stake():
        """
        Get initial stake of node.

        To use:
            .. code-block:: python

                initial_stake = await remme.node_management.get_initial_stake()
        """
        pass

    @staticmethod
    @abc.abstractmethod
    def get_node_account(node_account_address):
        """
        Get node account by node account address.

        Args:
            node_account_address (string): node account address

        To use:
            .. code-block:: python

                node_account = await remme.node_management.get_node_account(
                    node_account_address='116829be95c8bb240396446ec359d0d7f04d257b72aeb4ab1ecfe50cf36e400a96ab9c',
                )
        """
        pass

    @staticmethod
    @abc.abstractmethod
    def get_node_info():
        """
        Get information about node.

        To use:
            .. code-block:: python

                node_info = await remme.node_management.get_node_info()
        """
        pass

    @staticmethod
    @abc.abstractmethod
    def get_node_config():
        """
        Get node config.

        To use:
            .. code-block:: python

                node_config = await remme.node_management.get_node_config()
        """
        pass
