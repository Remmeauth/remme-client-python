from sawtooth_signing.secp256k1 import Secp256k1PrivateKey
from sawtooth_signing import create_context, CryptoFactory
from remme.remme_utils import hex_to_bytes, generate_address, RemmeFamilyName, is_hex
from remme.remme_patterns import RemmePatterns
import re


class RemmeAccount:
    """
    Account that is used for signing transactions and storing public keys which he was signed.
    @example
    ```python
    account = RemmeAccount(private_key_hex="ac124700cc4325cc2a78b22b9acb039d9efe859ef673b871d55d1078391934f9");
    print(account.private_key_hex); # "ac124700cc4325cc2a78b22b9acb039d9efe859ef673b871d55d1078391934f9";

    another_account = RemmeAccount();
    print(anotherAccount.private_key_hex) # "b5167700cc4325cc2a78b22b9acb039d9efe859ef673b871d55d10783919129f";

    data = "transaction data";
    signed_data = account.sign(data);

    is_verify = account.verify(signed_data, data);
    print(is_verify); // True

    is_verify_in_another_account = another_account.verify(signed_data, data);
    print(is_verify_in_another_account); // False
    ```
    """

    _context = None
    _family_name = None
    _signer = None
    _private_key_hex = None
    _private_key = None
    _public_key_hex = None
    _public_key = None
    _address = None

    def __init__(self, private_key_hex):
        """
        Get or generate private key, create signer by using private key,
        generate public key from private key and generate account address by using public key and family name
        (https://docs.remme.io/remme-core/docs/family-account.html#addressing)
        @example
        Get private key;
        ```python
        account = RemmeAccount("ac124700cc4325cc2a78b22b9acb039d9efe859ef673b871d55d1078391934f9");
        print(account.private_key_hex); // "ac124700cc4325cc2a78b22b9acb039d9efe859ef673b871d55d1078391934f9";
        ```

        Generate new private key;
        ```python
        account = RemmeAccount();
        print(account.private_key_hex); // "b5167700cc4325cc2a78b22b9acb039d9efe859ef673b871d55d10783919129f";
        ```
        :param private_key_hex: {string}
        """
        self._family_name = RemmeFamilyName.ACCOUNT.value
        if private_key_hex and re.match(RemmePatterns.PRIVATE_KEY.value, private_key_hex) is None:
            raise Exception("Invalid private key given!")
        self._context = create_context("secp256k1")
        if not private_key_hex:
            self._private_key = self._context.new_random_private_key()
        else:
            self._private_key = Secp256k1PrivateKey.from_hex(private_key_hex)

        self._signer = CryptoFactory(self._context).new_signer(self._private_key)
        self._private_key_hex = self._private_key.as_hex()
        self._private_key = Secp256k1PrivateKey.from_hex(self._private_key_hex)
        self._public_key = self._signer.get_public_key()
        self._public_key_hex = self._public_key.as_hex()
        self._address = generate_address(self._family_name, self._public_key_hex)

    @staticmethod
    def _validate_byte_message(message):
        if isinstance(message, bytes):
            return message
        if isinstance(message, str) and is_hex(message):
            return hex_to_bytes(message)
        raise Exception(f"Invalid type of message given. Expected hex string or bytes.")

    @staticmethod
    def _validate_string_hex_message(message):
        if isinstance(message, str) and is_hex(message):
            return message
        raise Exception(f"Invalid type of message given. Expected hex string.")

    def sign(self, transaction):
        """
        Get transaction and sign it by signer
        @example
        ```python
        data = "transaction data";
        signed_data = account.sign(data);
        print(signedData);
        ```
        :param transaction: {hex_encoded_string | bytes}
        :return: {hex_encoded_string}
        """
        transaction = self._validate_byte_message(transaction)
        return self._signer.sign(transaction)

    def verify(self, signature, transaction):
        """
        Verify given signature to given transaction
        @example
        ```python
        data = "transaction data";
        signed_data = account.sign(data);

        is_verify = account.verify(signed_data, data);
        print(is_verify); # True

        is_verify_in_another_account = another_account.verify(signed_data, data);
        print(is_verify_in_another_account); # False
        ```
        :param signature: {hex_encoded_string}
        :param transaction: {hex_encoded_string | bytes}
        :return: {boolean}
        """
        transaction = self._validate_byte_message(transaction)
        signature = self._validate_string_hex_message(signature)
        return self._context.verify(signature, transaction, self._public_key)

    @property
    def family_name(self):
        """
        Get constant account transaction's family name
        :return: {string}
        """
        return self._family_name

    @property
    def address(self):
        """
        Get address generated from public key hex
        :return: {bytes}
        """
        return self._address

    @property
    def public_key(self):
        """
        Get public key that that was generated from public key hex
        :return: {sawtooth_signing.secp256k1.Secp256k1PublicKey}
        """
        return self._public_key

    @property
    def public_key_hex(self):
        """
        Get public key hex that was generated automatically or given by user
        :return: {string}
        """
        return self._public_key_hex

    @property
    def private_key(self):
        """
        Get private key that was generated from user's public key
        :return: {sawtooth_signing.secp256k1.Secp256k1PrivateKey}
        """
        return self._private_key

    @property
    def private_key_hex(self):
        """
        Get private key hex that was generated from user's private key
        :return: {string}
        """
        return self._private_key_hex
