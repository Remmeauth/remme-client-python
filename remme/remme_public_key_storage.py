
class RemmePublicKeyStorage:
    """
    Class for working with public key storage.
    @example
    ```python
    remme = Remme()
    # if you don't have private and public keys you can generate them
    from remme.remme_utils import generate_rsa_key_pair
    private_key, public_key = generate_rsa_key_pair();
    store_response = await remme.public_key_storage.store(
         data="store data",
         private_key=private_key, # need for signing data
         public_key=public_key,
         valid_from=valid_from,
         valid_to=valid_to
    )
    async for msg in store_response.connect_to_web_socket():
        print(msg)

        key_is_valid = await remme.public_key_storage.check(public_key)
        print(key_is_valid) # True

        public_key_info = await remme.public_key_storage.get_info(public_key)
        print(public_key_info) # public_key_info

        revoke = await remme.public_key_storage.revoke(public_key)
        # You can connect_to_web_socket like in store method.
        print(revoke.batch_id) # r"\^[a-f0-9]{128}$\"

        public_keys = await remme.public_key_storage.get_account_public_keys(remme.account.public_key_hex)
        print(public_keys) # []

        store_response.close_web_socket()
    ```
    """

    _remme_api = None
    _remme_transaction = None
    _remme_account = None

    def __init__(self, remme_api, remme_account, remme_transaction):
        """
        @example
        Usage without remme main package
        ```python
        api = RemmeApi()
        account = RemmeAccount()
        transaction = RemmeTransactionService(api, account)
        public_key_storage = RemmePublicKeyStorage(rest, account, transaction)
        ```
        :param remme_api: RemmeApi
        :param remme_account: RemmeAccount
        :param remme_transaction: RemmeTransaction
        """
        self._remme_api = remme_api
        self._remme_transaction = remme_transaction
        self._remme_account = remme_account

    async def store(self, public_key_store_data):
        """
        Store public key with its data into REMChain.
        Send transaction to chain.
        @example
        ```python
        public_key_storage_data = PublicKeyStore(
             data="store data",
             private_key=private_key, # need for signing data
             public_key=public_key,
             valid_from=valid_from,
             valid_to=valid_to
        )
        store_response = await remme.public_key_storage.store(public_key_storage_data)
        async for msg in store_response.connect_to_web_socket():
            print(msg)
            store_response.close_web_socket()
        ```
        :param public_key_store_data: {PublicKeyStore}
        :return: {Promise BaseTransactionResponse}
        """
        raise NotImplementedError

    def check(self, public_key):
        raise NotImplementedError

    def revoke(self, public_key):
        raise NotImplementedError

    def get_user_public_key(self, user_account_public_key):
        raise NotImplementedError

    def generate_message(self, data):
        raise NotImplementedError

    def generate_entity_hash(self, message):
        raise NotImplementedError
