from remme.keys import RemmeKeys
from remme.models.general.methods import RemmeMethods
from remme.models.interfaces.public_key_storage import IRemmePublicKeyStorage
from remme.models.keys.key_type import KeyType
from remme.models.keys.rsa_signature_padding import RsaSignaturePadding
from remme.models.public_key_storage.public_key_info import PublicKeyInfo
from remme.models.utils.constants import CONSENSUS_ADDRESS
from remme.models.utils.family_name import RemmeFamilyName
from remme.protobuf.pub_key_pb2 import (
    NewPubKeyPayload,
    NewPubKeyStoreAndPayPayload,
    PubKeyMethod,
    RevokePubKeyPayload,
)
from remme.protobuf.transaction_pb2 import TransactionPayload
from remme.utils import (
    check_sha,
    generate_address,
    generate_settings_address,
    get_padding,
    public_key_address,
    sha512_hexdigest,
    validate_address,
)


class RemmePublicKeyStorage(IRemmePublicKeyStorage):
    """
    Class for working with public key storage.

    To use:
        .. code-block:: python

            from remme.models.keys.key_type import KeyType

            keys = await RemmeKeys.construct(KeyType.RSA)

            store_response = await remme.public_key_storage.create_and_store(
                data='store data',
                keys=keys,
                valid_from=valid_from,
                valid_to=valid_to,
                signature=signature,
                do_owner_pay=do_owner_pay,
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
    """

    _family_name = RemmeFamilyName.PUBLIC_KEY.value
    _family_version = '0.1'
    _settings_address = generate_settings_address(key='remme.economy_enabled')

    def __init__(self, remme_api, remme_account, remme_transaction_service):
        """
        Args:
            remme_api: RemmeAPI
            remme_account: RemmeAccount
            remme_transaction_service: RemmeTransactionService

        To use:
            Usage without remme main package.

            .. code-block:: python

                api = RemmeAPI()
                account = RemmeAccount()
                transaction = RemmeTransactionService()
                public_key_storage = RemmePublicKeyStorage(api, account, transaction)
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

    @staticmethod
    def _construct_address_from_payload(payload):

        entity_hash, entity_hash_signature = payload.entity_hash, payload.entity_hash_signature

        check_sha(data=sha512_hexdigest(payload.entity_hash))

        key_type = ''

        if payload.HasField('rsa'):
            key_type = KeyType.RSA

        elif payload.HasField('ecdsa'):
            key_type = KeyType.ECDSA

        elif payload.HasField('ed25519'):
            key_type = KeyType.EdDSA

        public_key = payload.rsa.key

        keys = RemmeKeys.construct(
            key_type=key_type,
            public_key=public_key,
        )

        if not keys.verify(data=entity_hash, signature=entity_hash_signature):
            raise Exception('Signature not valid.')

        return keys.address

    @staticmethod
    def _verify_payload_owner(owner_public_key, signature_by_owner, pub_key_payload):

        account_key = RemmeKeys.construct(
            key_type=KeyType.ECDSA,
            public_key=owner_public_key,
        )

        new_pub_key_payload = NewPubKeyPayload(
            entity_hash=pub_key_payload.entity_hash,
            entity_hash_signature=pub_key_payload.entity_hash_signature,
            valid_from=pub_key_payload.valid_from,
            valid_to=pub_key_payload.valid_to,
        )

        if pub_key_payload.HasField('rsa'):
            new_pub_key_payload_rsa = NewPubKeyPayload(rsa=pub_key_payload.rsa)
            new_pub_key_payload.MergeFrom(new_pub_key_payload_rsa)

        if pub_key_payload.HasField('ed25519'):
            new_pub_key_payload_eddsa = NewPubKeyPayload(rsa=pub_key_payload.ed25519)
            new_pub_key_payload.MergeFrom(new_pub_key_payload_eddsa)

        if pub_key_payload.HasField('ecdsa'):
            new_pub_key_payload_ecdsa = NewPubKeyPayload(rsa=pub_key_payload.ecdsa)
            new_pub_key_payload.MergeFrom(new_pub_key_payload_ecdsa)

        if not account_key.verify(data=new_pub_key_payload.SerializeToString(), signature=signature_by_owner):
            raise Exception('Owner signature not valid.')

    def create(self, data):
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

        Returns:
            Payload bytes.

        To use:
            .. code-block:: python

                from remme import Remme as remme
                from remme.models.keys.key_type import KeyType
                from remme.models.keys.rsa_signature_padding import RsaSignaturePadding

                keys = remme.keys.construct(KeyType.RSA)

                payload_bytes = remme.public_key_storage.create(
                    data='store data',
                    keys,
                    rsa_signature_padding=RsaSignaturePadding.PSS,
                    valid_from=int(datetime.now().timestamp()),
                    valid_to=int(CURRENT_TIMESTAMP + timedelta(365).total_seconds()),
                    do_owner_pay=False,
                )

            Create public key payload in bytes to store with private_key.

            .. code-block:: python

                from remme import Remme as remme
                from remme.models.keys.key_type import KeyType
                from remme.models.keys.rsa_signature_padding import RsaSignaturePadding

                keys = remme.keys.construct(KeyType.RSA)

                payload_bytes = remme.public_key_storage.create(
                    data='store data',
                    keys,
                    rsa_signature_padding=RsaSignaturePadding.PSS,
                    valid_from=int(datetime.now().timestamp()),
                    valid_to=int(CURRENT_TIMESTAMP + timedelta(365).total_seconds()),
                    do_owner_pay=True,
                )

            Create public key payload in bytes to store with another payer with public_key and signature.

            .. code-block:: python

                from remme import Remme as remme
                from remme.models.keys.key_type import KeyType
                from remme.models.keys.rsa_signature_padding import RsaSignaturePadding

                private_key, public_key = remme.keys.generate_key_pair(KeyType.RSA)

                keys_from_private = remme.keys.construct(
                    key_type=KeyType.ECDSA,
                    private_key=private_key,
                    public_key=public_key,
                )

                # Sign data with private_key

                data = 'test'
                signature = keys_from_private.sign(sha512(data))

                # Construct keys from public_key

                keys_from_public = remme.keys.construct(
                    key_type=KeyType.ECDSA,
                    public_key=public_key,
                )

                # Create public key payload with public_key only and signature.
                # To store keys with signature sign data should be in sha512 or sha256 format.

                payload_bytes = remme.public_key_storage.create(
                    data=sha512(data),
                    keys_from_public,
                    signature,
                    rsa_signature_padding=RsaSignaturePadding.PSS,
                    valid_from=int(datetime.now().timestamp()),
                    valid_to=int(CURRENT_TIMESTAMP + timedelta(365).total_seconds()),
                    do_owner_pay=False,
                )
        """
        keys = data.get('keys')

        public_key, key_type = keys.public_key, keys.key_type

        signature = data.get('signature')
        rsa_signature_padding = data.get('rsa_signature_padding')

        message = data.get('data') if signature else sha512_hexdigest(data=data.get('data'))

        if not signature:
            signature = keys.sign(data=message, rsa_signature_padding=rsa_signature_padding)

        entity_hash = message.encode('utf-8')
        entity_hash_signature = signature

        valid_from, valid_to = data.get('valid_from'), data.get('valid_to')

        pub_key_payload = NewPubKeyPayload(
            entity_hash=entity_hash,
            entity_hash_signature=entity_hash_signature,
            valid_from=valid_from,
            valid_to=valid_to,
            hashing_algorithm=NewPubKeyPayload.HashingAlgorithm.Value('SHA256'),
        )

        if key_type == KeyType.RSA:

            padding = get_padding(padding=rsa_signature_padding) if rsa_signature_padding else RsaSignaturePadding.PSS

            pub_key_payload_rsa = NewPubKeyPayload(
                rsa=NewPubKeyPayload.RSAConfiguration(
                    padding=padding,
                    key=public_key,
                ),
            )
            pub_key_payload.MergeFrom(pub_key_payload_rsa)

        if key_type == KeyType.EdDSA:

            pub_key_payload_eddsa = NewPubKeyPayload(
                ed25519=NewPubKeyPayload.Ed25519Configuration(key=public_key),
            )
            pub_key_payload.MergeFrom(pub_key_payload_eddsa)

        if key_type == KeyType.ECDSA:

            pub_key_payload_ecdsa = NewPubKeyPayload(
                ecdsa=NewPubKeyPayload.ECDSAConfiguration(
                    key=public_key,
                    ec=NewPubKeyPayload.ECDSAConfiguration.EC.Value('SECP256k1'),
                ),
            )
            pub_key_payload.MergeFrom(pub_key_payload_ecdsa)

        if data.get('do_owner_pay'):
            return pub_key_payload.SerializeToString()

        signature_by_owner = self._remme_account.sign(pub_key_payload.SerializeToString())

        new_pub_key_store_and_pay_payload = NewPubKeyStoreAndPayPayload(
            pub_key_payload=pub_key_payload,
            owner_public_key=bytes.fromhex(self._remme_account.public_key_hex),
            signature_by_owner=bytes.fromhex(signature_by_owner),
        )

        return new_pub_key_store_and_pay_payload.SerializeToString()

    async def store(self, data):
        """
        Store public key payload bytes with data into REMChain.
        Send transaction to chain.

        Args:
            data (object): payload bytes

        Returns:
            Information about storing public key to REMChain.

        To use:
            .. code-block:: python

                # payload_bytes is the transaction payload generated from method
                # remme.public_key_storage.create
                from remme import Remme as remme
                store_response = await remme.public_key_storage.store(payload_bytes)

                async for msg in store_response.connect_to_web_socket():
                    print(msg)
                    store_response.close_web_socket()
        """
        owner_address = ''

        owner_payload = NewPubKeyStoreAndPayPayload()
        owner_payload.ParseFromString(data)

        new_pub_key_payload = NewPubKeyPayload()
        new_pub_key_payload.ParseFromString(data)

        message = owner_payload if owner_payload.pub_key_payload.entity_hash else new_pub_key_payload

        if isinstance(message, NewPubKeyPayload):
            pub_key_address = self._construct_address_from_payload(payload=message)

        elif isinstance(message, NewPubKeyStoreAndPayPayload):

            owner_public_key = message.owner_public_key
            signature_by_owner = message.signature_by_owner
            pub_key_payload = message.pub_key_payload

            self._verify_payload_owner(
                owner_public_key=owner_public_key,
                signature_by_owner=signature_by_owner,
                pub_key_payload=pub_key_payload,
            )

            pub_key_address = self._construct_address_from_payload(payload=pub_key_payload)

            owner_address = generate_address(
                _family_name=RemmeFamilyName.ACCOUNT.value,
                _public_key_to=owner_public_key,
            )

        else:
            raise Exception('Invalid payload.')

        inputs_and_outputs = [
            pub_key_address,
            CONSENSUS_ADDRESS,
            self._settings_address
        ]

        if owner_address:
            inputs_and_outputs.append(owner_address)

        payload_bytes = self._generate_transaction_payload(
            method=PubKeyMethod.STORE_AND_PAY if owner_address else PubKeyMethod.STORE,
            data=data,
        )

        return await self._create_and_send_transaction(
            inputs=inputs_and_outputs,
            outputs=inputs_and_outputs,
            payload_bytes=payload_bytes,
        )

    async def create_and_store(self, **data):
        """
        Create public key payload bytes and store public key with its data into REMChain.
        Send transaction to chain with private key.

        Args:
            data (kwargs): data

        Returns:
            Information about storing public key to REMChain.

        To use:
            .. code-block:: python

                from remme.models.keys.key_type import KeyType

                keys = await RemmeKeys.construct(KeyType.RSA)
                store_response = await remme.public_key_storage.create_and_store(
                    data='store data',
                    keys=keys,
                    valid_from=valid_from,
                    valid_to=valid_to,
                    signature=signature,
                    do_owner_pay=do_owner_pay,
                )

                async for msg in store_response.connect_to_web_socket():
                    print(msg)

            Create public key payload bytes and store public key with its data into REMChain.
            Send transaction to chain with signature.

            .. code-block:: python

                from remme import Remme as remme
                from remme.models.keys.key_type import KeyType
                from remme.models.keys.rsa_signature_padding import RsaSignaturePadding

                private_key, public_key = remme.keys.generate_key_pair(KeyType.RSA)

                keys_from_private = remme.keys.construct(
                    key_type=KeyType.ECDSA,
                    private_key=private_key,
                    public_key=public_key,
                )

                # Sign data with private_key

                data = 'test'
                signature = keys_from_private.sign(sha512(data))

                # Construct keys from public_key

                keys_from_public = remme.keys.construct(
                    key_type=KeyType.ECDSA,
                    public_key=public_key,
                )

                # Create public key payload with public_key only and signature.
                # To store keys with signature sign data should be in sha512 or sha256 format.

                payload_bytes = remme.public_key_storage.create_and_store(
                    data=sha512(data),
                    keys_from_public,
                    signature,
                    rsa_signature_padding=RsaSignaturePadding.PSS,
                    valid_from=int(datetime.now().timestamp()),
                    valid_to=int(CURRENT_TIMESTAMP + timedelta(365).total_seconds()),
                    do_owner_pay=False,
                )
        """
        payload_bytes = self.create(data=data)
        return await self.store(data=payload_bytes)

    async def check(self, address):
        """
        Check public key on validity and revocation.
        Take address of public key.

        Args:
            address (string): address

        Returns:
            Boolean ``True``.

        To use:
            .. code-block:: python

                is_valid = await remme.public_key_storage.check(public_key_address)
        """
        try:
            await self._get_info_by_public_key(address=address)
            return True
        except Exception:
            return False

    async def get_info(self, public_key_address):
        """
        Get info about this public key.
        Take address of public key.

        Args:
            public_key_address (string): public key address

        Returns:
            Information about public key.

        To use:
            .. code-block:: python

                info = await remme.public_key_storage.get_info(public_key_address)
        """
        return await self._get_info_by_public_key(address=public_key_address)

    async def revoke(self, public_key_address):
        """
        Revoke public key by address.
        Take address of public key. Send transaction to chain.

        Args:
            public_key_address (string): public key address

        Returns:
            Information about revoked public key.

        To use:
            .. code-block:: python

                revoke_response = await remme.public_key_storage.revoke(public_key_address)
        """
        validate_address(address=public_key_address)

        revoke_payload = RevokePubKeyPayload(address=public_key_address).SerializeToString()
        payload_bytes = self._generate_transaction_payload(
            method=PubKeyMethod.REVOKE,
            data=revoke_payload,
        )

        inputs_and_outputs = [
            public_key_address,
            CONSENSUS_ADDRESS,
        ]

        return await self._create_and_send_transaction(
            inputs=inputs_and_outputs,
            outputs=inputs_and_outputs,
            payload_bytes=payload_bytes,
        )

    async def get_account_public_keys(self, address):
        """
        Take account address (which describe in RemmePatterns.ADDRESS).

        Args:
            address (string): address

        Returns:
            List with public key addresses.

        To use:
            .. code-block:: python

                public_key_addresses = await remme.public_key_storage.get_account_public_keys(remme.account.address)
        """
        validate_address(address=address)

        return await self._remme_api.send_request(
            method=RemmeMethods.USER_PUBLIC_KEY,
            params=public_key_address(address),
        )
