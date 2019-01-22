import math
from datetime import datetime, timedelta

from cryptography import x509
from cryptography.x509 import NameOID
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes

from remme.enums.rsa_signature_padding import RsaSignaturePadding
from remme.models.certificate_transaction_response import CertificateTransactionResponse
from remme.remme_certificate.interface import IRemmeCertificate
from remme.remme_certificate.x509_certificate_builder import X509CertificateBuilder
from remme.remme_keys.rsa import RSA
from remme.remme_utils import (
    certificate_from_pem,
    certificate_to_pem,
    private_key_to_der,
    public_key_to_der,
    private_key_der_to_object,
    public_key_der_to_object,
)


class RemmeCertificate(IRemmeCertificate):
    """
    Class for working with certificates, such as create, store, revoke, check, get_info.
    @example
    ```python
    remme = Remme()
    certificate_transaction_result = await remme.certificate.create_and_store({
        common_name='user_name',
        email='user@email.com',
        name='John',
        surname='Smith',
        country_name='US',
        validity=360,
        serial=str(datetime.now())
    })

    async for response in certificate_transaction_result.connect_to_web_socket():
        print('store', response)
        if response.status === 'COMMITTED':
            certificate_transaction_result.close_web_socket()
            status = await remme.certificate.check(certificate_transaction_result.certificate)
            print('status:', status) # True
            info = await remme.certificate.get_info(certificate_transaction_result.certificate)
            print('info:', info)
            revoke = await remme.certificate.revoke(certificate_transaction_result.certificate)
            async for res in revoke.connect_to_web_socket():
                print('revoke', response)
                if response.status === 'COMMITTED':
                    revoke.close_web_socket()
                    status = await remme.certificate.check(certificate_transaction_result.certificate)
                    print(status) # False
    ```
    """

    _rsa_key_size = 2048

    def __init__(self, remme_public_key_storage):
        """
        Usage without remme main package.
        @example
        ```python
        api = RemmeAPI()
        account = RemmeAccount()
        transaction = RemmeTransactionService()
        public_key_storage = RemmePublicKeyStorage(api, account, transaction)
        certificate = RemmeCertificate(public_key_storage)
        ```
        """
        self._remme_public_key_storage = remme_public_key_storage

    @staticmethod
    def get_params():
        """
        Get name attributes for subject creation.
        :return: name attributes: dict
        """
        return {
            'common_name': NameOID.COMMON_NAME,
            'email': NameOID.EMAIL_ADDRESS,
            'country_name': NameOID.COUNTRY_NAME,
            'locality_name': NameOID.LOCALITY_NAME,
            'postal_address': NameOID.POSTAL_ADDRESS,
            'postal_code': NameOID.POSTAL_CODE,
            'street_address': NameOID.STREET_ADDRESS,
            'state_name': NameOID.STATE_OR_PROVINCE_NAME,
            'name': NameOID.GIVEN_NAME,
            'surname': NameOID.SURNAME,
            'pseudonym': NameOID.PSEUDONYM,
            'generation_qualifier': NameOID.GENERATION_QUALIFIER,
            'title': NameOID.TITLE,
            'serial': NameOID.SERIAL_NUMBER,
            'business_category': NameOID.BUSINESS_CATEGORY,
        }

    def _create_subject(self, certificate_data_to_create):
        """
        Create subject for certificate.
        :param certificate_data_to_create: dict
        :return: subject
        """
        if certificate_data_to_create.get('common_name') is None:
            raise Exception('Attribute `common_name` must have a value.')

        if certificate_data_to_create.get('validity') is None:
            raise Exception('Attribute `validity` must have a value.')

        parameters = self.get_params()

        name_attributes = []

        for key, value in parameters.items():
            if key in certificate_data_to_create.keys():
                name_attributes.append(x509.NameAttribute(value, certificate_data_to_create[key]))

        return x509.Name(name_attributes)

    def _create_certificate(self, keys, certificate_data_to_create):
        """
        Create certificate and sign it.
        :param keys: RSA private and public key: bytes
        :param certificate_data_to_create: dict
        :return: signed certificate object
        """
        private_key, public_key = keys

        subject = issuer = self._create_subject(certificate_data_to_create)

        if 'validity_after' in certificate_data_to_create:
            not_valid_before = datetime.utcnow() + timedelta(days=certificate_data_to_create.get('validity_after'))
        else:
            not_valid_before = datetime.utcnow()

        if 'validity' in certificate_data_to_create:
            not_valid_after = not_valid_before + timedelta(days=certificate_data_to_create.get('validity'))
        else:
            not_valid_after = not_valid_before + timedelta(days=365)

        certificate_builder = X509CertificateBuilder(
            private_key=private_key_der_to_object(private_key),
            issuer_name=issuer,
            subject_name=subject,
            public_key=public_key_der_to_object(public_key),
            serial_number=x509.random_serial_number(),
            not_valid_before=not_valid_before,
            not_valid_after=not_valid_after,
        )

        certificate = certificate_builder.sign(
            private_key=certificate_builder.private_key, algorithm=hashes.SHA256(), backend=default_backend(),
        )

        certificate.private_key = certificate_builder.private_key

        return certificate

    def create(self, **certificate_data_to_create):
        """
        Create certificate.
        @example
        ```python
        certificate = remme.certificate.create(
            common_name='user_name',
            email='user@email.com',
            name='John',
            surname='Smith',
            country_name='US',
            validity=360,
            serial=str(datetime.now())
        )
        ```
        :param certificate_data_to_create: dict
        :return: signed certificate object
        """
        return self._create_certificate(
            keys=RSA.generate_key_pair(),
            certificate_data_to_create=certificate_data_to_create,
        )

    def create_and_store(self, certificate_data_to_create=None):
        """
        Method that creates certificate and stores it in to REMChain.
        Send transaction to chain.
        @example
        ```python
        remme = Remme()
        certificate_transaction_result = remme.certificate.create_and_store(
            common_name='user_name',
            email='user@email.com',
            name='John',
            surname='Smith',
            country_name='US',
            validity=360,
            serial=str(datetime.now())
        )
        ```
        :return: information about storing public key to REMChain
        """
        certificate = self.create(certificate_data_to_create=certificate_data_to_create)
        return self.store(certificate=certificate)

    async def store(self, certificate):
        """
        Store your certificate public key and hash of certificate into REMChain.
        Your certificate should contains private and public keys.
        Send transaction to chain.
        @example
        ```python
        remme = Remme()
        certificate = remme.certificate.create(
            common_name='user_name',
            email='user@email.com',
            name='John',
            surname='Smith',
            country_name='US',
            validity=360,
            serial=str(datetime.now())
        )
        store_response = remme.certificate.store(certificate)
        ```
        :param certificate: object
        :return: information about storing public key to REMChain
        """
        if type(certificate) == str:
            certificate = certificate_from_pem(certificate=certificate)

        certificate_pem = certificate_to_pem(certificate=certificate).decode('utf-8')

        valid_from = math.floor(int(certificate.not_valid_before.strftime("%s")) / 1000)
        valid_to = math.floor(int(certificate.not_valid_after.strftime("%s")) / 1000)

        batch_response = await self._remme_public_key_storage.store(
            data=certificate_pem,
            keys=RSA(
                private_key=private_key_to_der(certificate.private_key),
                public_key=public_key_to_der(certificate.public_key()),
            ),
            rsa_signature_padding=RsaSignaturePadding.PSS,
            valid_from=valid_from,
            valid_to=valid_to,
        )

        return CertificateTransactionResponse(
            node_address=batch_response.node_address,
            ssl_mode=batch_response.ssl_mode,
            batch_id=batch_response.batch_id,
            certificate=certificate,
        )

    def check(self, certificate):
        """
        Check certificate's public key on validity and revocation.
        @example
        ```python
        remme = Remme()
        is_valid = remme.certificate.check(certificate)
        ```
        :return: boolean
        """
        if type(certificate) == str:
            certificate = certificate_from_pem(certificate=certificate)

        address = RSA.get_address_from_public_key(
            public_key_to_der(public_key=certificate.public_key()),
        )

        check_result = self._remme_public_key_storage.check(address=address)

        if check_result is not None:
            return check_result
        else:
            raise Exception('This certificate was not found.')

    async def get_info(self, certificate):
        """
        Get info about certificate's public key.
        @example
        ```python
        remme = Remme()
        info = remme.certificate.get_info(certificate)
        ```
        :return: information about public key
        """
        if type(certificate) == str:
            certificate = certificate_from_pem(certificate=certificate)

        address = RSA.get_address_from_public_key(
            public_key_to_der(public_key=certificate.public_key()),
        )

        check_result = await self._remme_public_key_storage.get_info(public_key_address=address)

        if check_result is not None:
            return check_result
        else:
            raise Exception('This certificate was not found.')

    def revoke(self, certificate):
        """
        Revoke certificate's public key into REMChain.
        Send transaction to chain.
        @example
        ```python
        remme = Remme()
        revoke_response = remme.certificate.revoke(certificate)
        :param certificate: object
        :return: information about revoked public key
        """
        if type(certificate) == str:
            certificate = certificate_from_pem(certificate=certificate)

        address = RSA.get_address_from_public_key(
            public_key_to_der(public_key=certificate.public_key()),
        )

        return self._remme_public_key_storage.revoke(public_key_address=address)

    def sign(self, certificate, data, rsa_signature_padding=None):
        """
        Sign data with a certificate's private key and output DigestInfo DER-encoded bytes (default for PSS).
        :param certificate: object
        :param data: string
        :param rsa_signature_padding: RsaSignaturePadding
        :return: signature
        """
        if type(certificate) == str:
            certificate = certificate_from_pem(certificate=certificate)

        if certificate.private_key is None:
            raise Exception('Your certificate does not have private key.')

        keys = RSA(private_key=private_key_to_der(certificate.private_key))

        return keys.sign(data=data, rsa_signature_padding=rsa_signature_padding)

    def verify(self, certificate, data, signature, rsa_signature_padding=None):
        """
        Verify data with a public key (default for PSS).
        :param certificate: object
        :param data: string
        :param signature: string
        :param rsa_signature_padding: RsaSignaturePadding
        :return: boolean
        """
        if type(certificate) == str:
            certificate = certificate_from_pem(certificate=certificate)

        if certificate.private_key is None:
            raise Exception('Your certificate does not have private key.')

        keys = RSA(public_key=public_key_to_der(certificate.public_key()))

        return keys.verify(data=data, signature=signature, rsa_signature_padding=rsa_signature_padding)
