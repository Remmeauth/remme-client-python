"""
Provide tests for token utils implementation.
"""
from remme.remme_utils import (
    is_address_valid,
    is_amount_valid,
    is_public_key_valid,
)


def test_is_amount_valid():
    """
    Case: check, is amount valid.
    Expect: True and None, error was not presented.
    """
    expected_result, result = (True, None), is_amount_valid(amount=100)

    assert expected_result == result


def test_is_amount_with_string_valid():
    """
    Case: check, is amount with string valid.
    Expect: false and amount is not an integer type error message.
    """
    expected_result, result = (False, 'Given amount is not in integer type.'), is_amount_valid(amount='100')

    assert expected_result == result


def test_is_amount_with_negative_number_valid():
    """
    Case: check, is amount with negative number valid.
    Expect: false and amount is not valid for operations error message.
    """
    expected_result, result = (False, 'Given amount is not valid for operations.'), is_amount_valid(amount=-10)

    assert expected_result == result


def test_is_address_valid():
    """
    Case: check, is address valid.
    Expect: True and None, error was not presented.
    """
    expected_result = True, None
    result = is_address_valid(address='1120077f88b0b798347b3f52751bb99fa8cabaf926c5a1dad2d975d7b966a85b3a9c21')

    assert expected_result == result


def test_is_address_with_empty_string_valid():
    """
    Case: check, is address with empty string valid.
    Expect: false and address was not provided error message.
    """
    expected_result = False, 'Address was not provided, please set the address.'
    result = is_address_valid(address='')

    assert expected_result == result


def test_is_address_with_invalid_length_valid():
    """
    Case: check, is address with invalid length valid.
    Expect: false and length of the address is not valid error message.
    """
    expected_result = False, 'Length of the given address is not valid.'
    result = is_address_valid(address='1120077f88b0b798347b3f52751bb99fa8cabaf926c5a1dad2d')

    assert expected_result == result


def test_is_address_not_in_hexadecimal_string_valid():
    """
    Case: check, is address not in hexadecimal string format valid.
    Expect: false and address is not in hexadecimal string error message.
    """
    expected_result = False, 'Given address is not in hexadecimal string format.'
    result = is_address_valid(address='1120077f88b0b798347b3f52751bb99fa8cabaf926c5a1dad2d975d7b966a85b239xor')

    assert expected_result == result


def test_is_public_key_valid():
    """
    Case: check, is public key valid.
    Expect: True and None, error was not presented.
    """
    expected_result = True, None
    result = is_public_key_valid(public_key='03ba3b69c5f7cf2c0dac39b93dee0d270277115e4926a53552813c6abdb07e96b2')

    assert expected_result == result


def test_is_public_key_with_empty_string_valid():
    """
    Case: check, is public key with empty string valid.
    Expect: false and public key was not provided error message.
    """
    expected_result = False, 'Public key was not provided, please set the public key.'
    result = is_public_key_valid(public_key='')

    assert expected_result == result


def test_is_public_key_with_invalid_length_valid():
    """
    Case: check, is public key with invalid length valid.
    Expect: false and length of the public key is not valid error message.
    """
    expected_result = False, 'Length of the given public key is not valid.'
    result = is_public_key_valid(public_key='03ba3b69c5f7cf2c0dac39b93dee0d270277115e4926a5355')

    assert expected_result == result


def test_is_public_key_not_in_hexadecimal_string_valid():
    """
    Case: check, is public key not in hexadecimal string format valid.
    Expect: false and public key is not in hexadecimal string error message.
    """
    expected_result = False, 'Given public key is not in hexadecimal string format.'
    result = is_public_key_valid(public_key='03ba3b69c5f7cf2c0dac39b93dee0d270277115e4926a53552813c6abdb07co7xz')

    assert expected_result == result
