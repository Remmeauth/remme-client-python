from remme.models.account.account_type import AccountType
from remme.models.keys.ecdsa import ECDSA
from remme.models.utils.family_name import RemmeFamilyName
from remme.utils import (
    generate_address,
    hex_to_bytes,
)

DEFAULT_ACCOUNT_CONFIG = {
    'private_key_hex': '',
    'account_type': AccountType.USER,
}


class RemmeAccount(ECDSA):
    """
    Account that is used for signing transactions and storing public keys which he was signed.

    To use:
        .. code-block:: python

            private_key_hex = 'ac124700cc4325cc2a78b22b9acb039d9efe859ef673b871d55d1078391934f9'
            account = RemmeAccount(private_key_hex)
            print(account.private_key_hex)
            # 'ac124700cc4325cc2a78b22b9acb039d9efe859ef673b871d55d1078391934f9'

            another_account = RemmeAccount()
            print(another_account.private_key_hex)
            # 'b5167700cc4325cc2a78b22b9acb039d9efe859ef673b871d55d10783919129f'

            data = 'some data'
            signed_data = account.sign(data)
            print(signed_data)  # signature

            is_verify = account.verify(data, signed_data)
            print(is_verify)  # True

            is_verify_in_another_account = another_account.verify(data, signed_data)
            print(is_verify_in_another_account)  # False
    """

    def __init__(self, private_key_hex='', account_type=AccountType.USER):
        """
        Get private key, create signer by using private key,
        generate public key from private key and generate account address by using public key and family name.

        Args:
            private_key_hex (string): private key in hex format
            account_type (enum): account type (user, node)

        References::
            - https://docs.remme.io/remme-core/docs/family-account.html#addressing

        To use:
            **Get private key:**

            .. code-block:: python

                private_key_hex = 'ac124700cc4325cc2a78b22b9acb039d9efe859ef673b871d55d1078391934f9'
                account = RemmeAccount()
                print(account.private_key_hex)
                # 'ac124700cc4325cc2a78b22b9acb039d9efe859ef673b871d55d1078391934f9'

            **Generate new private key:**

            .. sourcecode:: python

                account = RemmeAccount()
                print(account.private_key_hex)
                # 'b5167700cc4325cc2a78b22b9acb039d9efe859ef673b871d55d10783919129f'
        """
        if private_key_hex:
            private_key = hex_to_bytes(private_key_hex)
        else:
            private_key, _ = ECDSA.generate_key_pair()

        super(RemmeAccount, self).__init__(private_key=private_key)

        is_user = account_type == AccountType.USER

        self._family_name = RemmeFamilyName.ACCOUNT.value if is_user else RemmeFamilyName.NODE_ACCOUNT.value
        self._address = generate_address(self._family_name, self._public_key_hex)
