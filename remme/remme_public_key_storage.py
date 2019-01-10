from remme.enums.remme_family_name import RemmeFamilyName
from remme.enums.remme_methods import RemmeMethods
from remme.enums.rsa_signature_padding import RsaSignaturePadding
from remme.models.public_key_info import PublicKeyInfo
from remme.protos.pub_key_pb2 import (
    PubKeyMethod,
    RevokePubKeyPayload,
)
from remme.protos.transaction_pb2 import TransactionPayload
from remme.remme_utils import (
    generate_address,
    generate_ecdsa_payload,
    generate_eddsa_payload,
    generate_rsa_payload,
    generate_settings_address,
    public_key_address,
    public_key_to_der,
    validate_address,
)
from remme.remme_keys.rsa import RSA
from remme.remme_keys.ecdsa import ECDSA
from remme.remme_keys.eddsa import EdDSA

ZERO_ADDRESS = '0' * 70


class RemmePublicKeyStorage:
    """
    Class for working with public key storage.

    @example
    ```python
    from remme.enums.key_type import KeyType

    keys = await RemmeKeys.construct(KeyType.RSA)

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

        revoke = await remme.public_key_storage.revoke(remme_keys.address)
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

        validate_address(address=address)

        info = await self._remme_api.send_request(
            method=RemmeMethods.PUBLIC_KEY,
            params=public_key_address(address),
        )

        if info.get('error') is None:
            info['address'] = generate_address(self._family_name, address)
            return PublicKeyInfo(data=info)

        raise Exception('This public key was not found.')

    async def store(self, data, keys, valid_from, valid_to, rsa_signature_padding=RsaSignaturePadding.PSS):
        """
        Store public key with its data into REMChain.
        Send transaction to chain.
        @example
        ```python
        from remme.remme import Remme
        from remme.enums.key_type import KeyType
        from remme.enums.rsa_signature_padding import RsaSignaturePadding

        keys = Remme.keys.construct(KeyType.RSA)

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
        if isinstance(keys, RSA):
            public_key = public_key_to_der(keys.public_key)
            new_pub_key_payload = generate_rsa_payload(
                message=data,
                keys=keys,
                public_key=public_key,
                valid_from=valid_from,
                valid_to=valid_to,
                rsa_signature_padding=rsa_signature_padding,
            )

        elif isinstance(keys, EdDSA):
            public_key = keys.public_key
            new_pub_key_payload = generate_eddsa_payload(
                message=data,
                keys=keys,
                public_key=public_key,
                valid_from=valid_from,
                valid_to=valid_to,
            )

        elif isinstance(keys, ECDSA):
            public_key = keys.public_key
            new_pub_key_payload = generate_ecdsa_payload(
                message=data,
                keys=keys,
                public_key=public_key,
                valid_from=valid_from,
                valid_to=valid_to,
            )

        else:
            raise Exception('Key type does not exist.')

        payload_bytes = self._generate_transaction_payload(
            method=PubKeyMethod.STORE,
            data=new_pub_key_payload.SerializeToString(),
        )

        storage_public_key_address = generate_address(self._family_name, public_key)
        economy_enabled_address = generate_settings_address("remme.economy_enabled")

        inputs = [
            storage_public_key_address,
            economy_enabled_address,
            ZERO_ADDRESS,
        ]

        outputs = [
            storage_public_key_address,
            ZERO_ADDRESS,
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

    async def get_info(self, public_key_address):
        """
        Get info about this public key.
        Take address of public key.
        @example
        ```python
        info = await remme.public_key_storage.get_info(public_key_address)
        ```
        :param public_key_address: string
        :return: information about public key
        """
        return await self._get_info_by_public_key(address=public_key_address)

    async def revoke(self, public_key_address):
        """
        Revoke public key by address.

        Take address of public key. Send transaction to chain.
        @example
        ```python
        revoke_response = await remme.public_key_storage.revoke(public_key_address)
        ```
        :param public_key_address: string
        :return: information about revoked public key
        """
        validate_address(address=public_key_address)

        revoke_payload = RevokePubKeyPayload(address=public_key_address).SerializeToString()
        payload_bytes = self._generate_transaction_payload(
            method=PubKeyMethod.REVOKE,
            data=revoke_payload,
        )

        return await self._create_and_send_transaction(
            inputs=[public_key_address],
            outputs=[public_key_address],
            payload_bytes=payload_bytes,
        )

    async def get_account_public_keys(self, address):
        """
        Take account address (which describe in PATTERNS.ADDRESS).
        @example
        ```python
        remme = Remme()
        public_key_addresses = await remme.public_key_storage.get_account_public_keys(remme.account.address)
        ```
        :param address: string
        :return: list with public key addresses
        """
        validate_address(address=address)

        return await self._remme_api.send_request(
            method=RemmeMethods.USER_PUBLIC_KEY,
            params=public_key_address(address),
        )
