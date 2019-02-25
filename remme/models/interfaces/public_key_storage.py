import abc


class IRemmePublicKeyStorage(metaclass=abc.ABCMeta):

    @staticmethod
    @abc.abstractmethod
    def create(data):
        """
        Create public key payload in bytes to store with another payer, private_key and public_key.

        Args:
            data (dict): data(
                data: string
                keys: object
                signature: string (optional)
                rsa_signature_padding: paddingRSA (optional)
                valid_from: int
                valid_to: int
                do_owner_pay: boolean (optional)
            )
        """
        pass

    @staticmethod
    @abc.abstractmethod
    def store(data):
        """
        Store public key payload bytes with data into REMChain.
        Send transaction to chain.

        Args:
            data (object): payload bytes
        """
        pass

    @staticmethod
    @abc.abstractmethod
    def create_and_store(data):
        """
        Create public key payload bytes and store public key with its data into REMChain.
        Send transaction to chain with private key.

        Args:
            data (dict): data(
                data: string
                keys: object
                signature: string (optional)
                rsa_signature_padding: paddingRSA (optional)
                valid_from: int
                valid_to: int
                do_owner_pay: boolean (optional)
            )
        """
        pass

    @staticmethod
    @abc.abstractmethod
    def check(address):
        """
        Check public key on validity and revocation.
        Take address of public key.

        Args:
            address (string): address
        """
        pass

    @staticmethod
    @abc.abstractmethod
    def revoke(public_key_address):
        """
        Revoke public key by address.
        Take address of public key. Send transaction to chain.

        Args:
            public_key_address (string): public key address
        """
        pass

    @staticmethod
    @abc.abstractmethod
    def get_info(public_key_address):
        """
        Get info about this public key.
        Take address of public key.

        Args:
            public_key_address (string): public key address
        """
        pass

    @staticmethod
    @abc.abstractmethod
    def get_account_public_keys(address):
        """
        Take account address (which describe in RemmePatterns.ADDRESS).

        Args:
            address (string): address
        """
        pass
