from remme.models.utils.family_name import RemmeFamilyName
from remme.models.keys.ecdsa import ECDSA
from remme.utils import (
    generate_address,
    hex_to_bytes,
)


class RemmeAccount(ECDSA):
    """
    Account that is used for signing transactions and storing public keys which he was signed.
    @example
    ```python
    account = RemmeAccount('ac124700cc4325cc2a78b22b9acb039d9efe859ef673b871d55d1078391934f9')
    print(account.private_key_hex)  # 'ac124700cc4325cc2a78b22b9acb039d9efe859ef673b871d55d1078391934f9'

    another_account = RemmeAccount()
    print(another_account.private_key_hex)  # 'b5167700cc4325cc2a78b22b9acb039d9efe859ef673b871d55d10783919129f'

    data = 'some data'
    signed_data = account.sign(data)

    is_verify = account.verify(data, signed_data)
    print(is_verify)  # True

    is_verify_in_another_account = another_account.verify(data, signed_data)
    print(is_verify_in_another_account)  # False
    ```
    """

    def __init__(self, private_key_hex):
        """
        Get private key, create signer by using private key,
        generate public key from private key and generate account address by using public key and family name.

        References:
            - https://docs.remme.io/remme-core/docs/family-account.html#addressing

        @example
        Get private key
        ```python
        account = RemmeAccount('ac124700cc4325cc2a78b22b9acb039d9efe859ef673b871d55d1078391934f9')
        print(account.private_key_hex)  # 'ac124700cc4325cc2a78b22b9acb039d9efe859ef673b871d55d1078391934f9'
        ```

        Generate new private key
        ```python
        account = RemmeAccount()
        print(account.private_key_hex) # 'b5167700cc4325cc2a78b22b9acb039d9efe859ef673b871d55d10783919129f'
        ```
        :param private_key_hex (optional): string
        """
        if private_key_hex:
            private_key = hex_to_bytes(private_key_hex)
        else:
            private_key, _ = ECDSA.generate_key_pair()

        super(RemmeAccount, self).__init__(private_key=private_key)

        self._family_name = RemmeFamilyName.ACCOUNT.value
        self._address = generate_address(self._family_name, self._public_key_hex)
