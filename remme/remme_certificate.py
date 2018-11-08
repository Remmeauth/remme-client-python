from remme.models.certificate_transaction_response import CertificateTransactionResponse


class RemmeCertificate:
    """
    Class for working with certificates, such as create, store, revoke, check, getInfo.
    @example
    ```python
    remme = Remme()
    certificate_transaction_result = await remme.certificate.create_and_store({
        common_name: "username",
        email: "user@email.com",
        name: "John",
        surname: "Smith",
        country_name: "US",
        validity: 360,
        serial: `${Date.now()}`
    })

    async for response in certificate_transaction_result.connect_to_web_socket():
        print("store", response)
        if response.status === "COMMITTED":
            certificate_transaction_result.close_web_socket()
            status = await remme.certificate.check(certificate_transaction_result.certificate)
            print('status:', status) # True
            info = await remme.certificate.get_info(certificate_transaction_result.certificate)
            print("info:", info)
            revoke = await remme.certificate.revoke(certificate_transaction_result.certificate)
            async for res in revoke.connect_to_web_socket():
                print("revoke", response)
                if res.status === "COMMITTED":
                    revoke.close_web_socket()
                    status = await remme.certificate.check(certificate_transaction_result.certificate)
                    print(status) # False

    ```
    """

    _rsa_key_size = 2048
    remme_public_key_storage = None

    def __init__(self, remme_public_key_storage):
        """
        Usage without remme main package
        ```python
        api = RemmeApi()
        account = RemmeAccount()
        transaction = RemmeTransactionService(api, account)
        public_key_storage = RemmePublicKeyStorage(api, account, transaction)
        certificate = RemmeCertificate(public_key_storage)
        ```
        :param remme_public_key_storage: {IRemmePublicKeyStorage}
        """
        self.remme_public_key_storage = remme_public_key_storage

    def _create_certificate(self, keys, create_certificate_dto):
        raise NotImplementedError

    async def create(self, create_certificate_dto):
        keys = await generateRSAKeyPair(self._rsa_key_size)
        return self._create_certificate(keys, create_certificate_dto)

    async def store(self, certificate):
        raise NotImplementedError

    async def create_and_store(self, create_certificate_dto):
        certificate = await self.create(create_certificate_dto)
        batch_response = await self.store(certificate)
        cert_response = CertificateTransactionResponse(
            node_address=batch_response.node_address,
            ssl_mode=batch_response.ssl_mode,
            batch_id=batch_response.batch_id
        )
        cert_response.certificate = certificate
        return cert_response

    def check(self, certificate):
        raise NotImplementedError

    def get_info(self):
        raise NotImplementedError

    def revoke(self, certificate):
        raise NotImplementedError

    def sign(self):
        raise NotImplementedError

    def verify(self):
        raise NotImplementedError
