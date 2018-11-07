from remme.constants.remme_family_name import RemmeFamilyName
from remme.models.create_transactions_d_to import CreateTransactionDto
from remme.protos.proto_buf_pb2 import NewPubKeyPayload, PubKeyMethod
from remme.protos.transaction_pb2 import TransactionPayload
from remme.remme_utils import generate_address, generate_settings_address


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
    _family_name = RemmeFamilyName.PUBLIC_KEY.value
    _family_version = "0.1"

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

    async def store(self, _data):
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
        :param _data: {PublicKeyStore}
        :return: {Promise BaseTransactionResponse}
        """
        public_key = public_key_to_pem(_data.public_key) if isinstance(_data.public_key, object) else _data.public_key
        private_key = private_key_from_pem(_data.private_key) if isinstance(_data.private_key,
                                                                            str) else _data.private_key
        message = self.generate_message(_data.data)
        entity_hash = self.generate_entity_hash(message)
        entity_hash_signature = self._generate_signature(entity_hash, private_key)
        payload = NewPubKeyPayload(
            public_key=public_key,
            public_key_type=_data.public_key_type,
            entity_type=_data.entity_type,
            entity_hash=entity_hash,
            entity_hash_signature=entity_hash_signature,
            valid_from=_data.valid_from,
            valid_to=_data.valid_to
        ).SerializeToString()
        pub_key_address = generate_address(self._family_name, public_key)
        storage_pub_key = generate_settings_address("remme.settings.storage_pub_key")
        setting_address = generate_settings_address("remme.economy_enabled")
        storage_address = generate_address(self._remme_account.family_name, storage_pub_key)
        payload_bytes = self._generate_transaction_payload(PubKeyMethod.STORE, payload)
        return await self._create_and_send_transaction([pub_key_address, storage_pub_key, setting_address,
                                                        storage_address], payload_bytes)

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

    def _generate_signature(self, data, private_key):
        raise NotImplementedError

    def _generate_transaction_payload(self, method, data):
        return TransactionPayload(method=method, data=data).SerializeToString()

    async def _create_and_send_transaction(self, inputs_and_outputs, payload_bytes):
        transaction_dto = CreateTransactionDto(family_name=self._family_name,
                                               family_version=self._family_version,
                                               inputs=[inputs_and_outputs],
                                               outputs=[inputs_and_outputs],
                                               payload_bytes=payload_bytes)
        transaction = await self._remme_transaction.create(transaction_dto)
        return await self._remme_transaction.send(transaction)
