import binascii

from remme.enums.remme_family_name import RemmeFamilyName
from remme.enums.remme_methods import RemmeMethods
from remme.enums.rsa_signature_padding import RsaSignaturePadding
from remme.models.public_key_info import PublicKeyInfo
from remme.models.public_key_request import PublicKeyRequest
from remme.protos.pub_key_pb2 import (
    NewPubKeyPayload,
    PubKeyMethod,
    RevokePubKeyPayload,
)
from remme.protos.transaction_pb2 import TransactionPayload
from remme.remme_utils import (
    generate_address,
    generate_settings_address,
    sha512_hexdigest,
    validate_address,
)


class RemmePublicKeyStorage:
    """
    Class for working with public key storage.

    @example
    ```python
    from remme.enums.key_type import KeyType

    keys = await RemmeKeys.genarate_key_pair(KeyType.RSA)

    store_response = await remme.public_key_storage.store(
        data='store data',
        keys=keys,
        valid_from=valid_from,
        valid_to=valid_to,
    )

    async for msg in store_response.connect_to_web_socket():
        print(msg)

        key_is_valid = await remme.public_key_storage.check(keys.address)
        print(key_is_valid)  # True

        public_key_info = await remme.public_key_storage.get_info(keys.address)
        print(public_key_info)  # PublicKeyInfo

        revoke = await remme.public_key_storage.revoke(keys.address)
        # You can connect_to_web_socket like in store method.
        print(revoke.batch_id)  # r"\^[a-f0-9]{128}$\"

        public_key_addresses = await remme.publicKeyStorage.get_account_public_keys(remme.account.address)
        print(public_key_addresses)  # []

        store_response.close_web_socket()
    ```
    """

    _family_name = RemmeFamilyName.PUBLIC_KEY.value
    _family_version = '0.1'

    def __init__(self, remme_api, remme_account, remme_transaction_service):
        """
        @example
        Usage without remme main package.
        ```python
        api = RemmeAPI()
        account = RemmeAccount()
        transaction = RemmeTransactionService()
        public_key_storage = RemmePublicKeyStorage(api, account, transaction)
        ```
        :param remme_api: RemmeAPI
        :param remme_account: RemmeAccount
        :param remme_transaction_service: RemmeTransactionService
        """
        self._remme_api = remme_api
        self._remme_account = remme_account
        self._remme_transaction = remme_transaction_service

    @staticmethod
    def _generate_transaction_payload(method, data):
        return TransactionPayload(method=method, data=data).SerializeToString()

    async def _create_and_send_transaction(self, inputs, outputs, payload_bytes):

        transaction = await self._remme_transaction.create(
            family_name=self._family_name,
            family_version=self._family_version,
            inputs=inputs,
            outputs=outputs,
            payload_bytes=payload_bytes,
        )
        return await self._remme_transaction.send(payload=transaction)

    async def _get_info_by_public_key(self, address):
        payload = PublicKeyRequest(address)

        info = await self._remme_api.send_request(
            method=RemmeMethods.PUBLIC_KEY,
            params=payload,
        )

        if info.get('error') is None:
            return PublicKeyInfo(data=info)

        raise Exception('This public key was not found.')

    async def store(self, data, keys, valid_from, valid_to, rsa_signature_padding=RsaSignaturePadding.PSS):
        """
        Store public key with its data into REMChain.
        Send transaction to chain.
        @example
        ```python
        from remme.enums.key_type import KeyType
        from remme.enums.rsa_signature_padding import RsaSignaturePadding

        keys = RemmeKeys.genarate_key_pair(KeyType.RSA)

        store_response = await remme.public_key_storage.store(
            data='store data',
            keys=keys,
            valid_from=valid_from,
            valid_to=valid_to,
            rsa_signature_padding=RsaSignaturePadding.PSS,
        )

        async for msg in store_response.connect_to_web_socket():
            print(msg)
            store_response.close_web_socket()
        ```
        :param data: string
        :param keys: instance of key class
        :param valid_from: timestamp
        :param valid_to: timestamp
        :param rsa_signature_padding: RsaSignaturePadding.PSS by default
        :return: information about storing public key to REMChain
        """
        message = sha512_hexdigest(data=data)
        entity_hash = binascii.unhexlify(message)
        entity_hash_signature = keys.sign(
            data=message,
            rsa_signature_padding=rsa_signature_padding,
        ).decode('hex')

        entity_type = NewPubKeyPayload.EntityType.PERSONAL.value
        public_key_type = NewPubKeyPayload.PubKeyType.RSA.value

        payload = NewPubKeyPayload(
            public_key=keys.public_key,
            public_key_type=public_key_type,
            entity_type=entity_type,
            entity_hash=entity_hash,
            entity_hash_signature=entity_hash_signature,
            valid_from=valid_from,
            valid_to=valid_to,
        ).SerializeToString()

        public_key_address = keys.address
        storage_public_key_address = generate_settings_address('remme.settings.storage_pub_key')
        setting_address = generate_settings_address('remme.economy_enabled')
        storage_address = generate_address(
            _family_name=self._remme_account.family_name,
            _public_key_to=storage_public_key_address,
        )

        payload_bytes = self._generate_transaction_payload(
            method=PubKeyMethod.Method.STORE,
            data=payload,
        )

        inputs = [
            public_key_address,
            storage_public_key_address,
            setting_address,
            storage_address,
        ]

        outputs = [
            public_key_address,
            storage_address,
        ]

        return await self._create_and_send_transaction(
            inputs=inputs,
            outputs=outputs,
            payload_bytes=payload_bytes,
        )

    async def check(self, address):
        """
        Check public key on validity and revocation.
        Take address of public key.
        @example
        ```python
        is_valid = await remme.public_key_storage.check(public_key_address)
        ```
        :param address: string
        :return: boolean
        """
        is_valid = self._get_info_by_public_key(address=address)
        return is_valid

    async def get_info(self, address):
        """
        Get info about this public key.
        Take address of public key.
        @example
        ```python
        info = await remme.public_key_storage.get_info(public_key_address)
        ```
        :param address: string
        :return: information about public key
        """
        return await self._get_info_by_public_key(address=address)

    async def revoke(self, public_key_address):
        """
        Revoke public key by address.

        Take address of public key. Send transaction to chain.
        @example
        ```python
        revoke_response = await remme.public_key_storage.revoke(public_key_address)
        ```
        :param public_key_address: string
        :return:
        """
        validate_address(address=public_key_address)

        revoke_payload = RevokePubKeyPayload(address=public_key_address).SerializeToString()
        payload_bytes = self._generate_transaction_payload(
            method=PubKeyMethod.Method.REVOKE,
            data=revoke_payload,
        )

        return await self._create_and_send_transaction(
            inputs=public_key_address,
            outputs=public_key_address,
            payload_bytes=payload_bytes,
        )

    async def get_account_public_keys(self, address):
        """
        Take account address (which describe in PATTERNS.ADDRESS).
        @example
        ```python
        public_key_addresses = await remme.public_key_storage.get_account_public_keys(remme.account.address)
        ```
        :param address: string
        :return: array with public key addresses
        """
        validate_address(address=address)

        payload = PublicKeyRequest(address)

        return await self._remme_api.send_request(
            method=RemmeMethods.USER_PUBLIC_KEY,
            params=payload,
        )
