"""
Provide tests for token utils implementation.
"""
import pytest

from remme.utils import (
    validate_address,
    validate_amount,
    validate_public_key,
)


def test_validate_amount():
    """
    Case: validate amount.
    Expect: None, error was not presented.
    """
    expected_result, result = None, validate_amount(amount=100)

    assert expected_result == result


def test_validate_amount_with_string():
    """
    Case: validate amount with string.
    Expect: amount is not an integer type error message.
    """
    expected_result = 'Given amount is not in integer type.'

    with pytest.raises(Exception) as error:
        validate_amount(amount='100')

    assert expected_result == str(error.value)


def test_validate_amount_with_negative_number():
    """
    Case: validate amount with negative number.
    Expect: amount is not valid for operations error message.
    """
    expected_result = 'Given amount must be higher than 0.'

    with pytest.raises(Exception) as error:
        validate_amount(amount=-10)

    assert expected_result == str(error.value)


def test_validate_address():
    """
    Case: validate address.
    Expect: None, error was not presented.
    """
    expected_result = None
    result = validate_address(address='1120077f88b0b798347b3f52751bb99fa8cabaf926c5a1dad2d975d7b966a85b3a9c21')

    assert expected_result == result


def test_validate_address_with_empty_string():
    """
    Case: validate address with empty string.
    Expect: address was not provided error message.
    """
    expected_result = 'Address was not provided, please set the address.'

    with pytest.raises(Exception) as error:
        validate_address(address='')

    assert expected_result == str(error.value)


def test_validate_address_with_invalid_length():
    """
    Case: validate address with invalid length.
    Expect: length of the address is not valid error message.
    """
    expected_result = 'Length of the given address is not valid.'

    with pytest.raises(Exception) as error:
        validate_address(address='1120077f88b0b798347b3f52751bb99fa8cabaf926c5a1dad2d')

    assert expected_result == str(error.value)


def test_validate_address_not_in_hexadecimal_string():
    """
    Case: validate address not in hexadecimal string format.
    Expect: address is not in hexadecimal string error message.
    """
    expected_result = 'Given address is not in hexadecimal string format.'

    with pytest.raises(Exception) as error:
        validate_address(address='1120077f88b0b798347b3f52751bb99fa8cabaf926c5a1dad2d975d7b966a85b239xor')

    assert expected_result == str(error.value)


def test_validate_public_key():
    """
    Case: validate public key.
    Expect: None, error was not presented.
    """
    expected_result = None
    result = validate_public_key(public_key='03ba3b69c5f7cf2c0dac39b93dee0d270277115e4926a53552813c6abdb07e96b2')

    assert expected_result == result


def test_validate_public_key_with_empty_string():
    """
    Case: validate public key with empty string.
    Expect: public key was not provided error message.
    """
    expected_result = 'Public key was not provided, please set the public key.'

    with pytest.raises(Exception) as error:
        validate_public_key(public_key='')

    assert expected_result == str(error.value)


def test_validate_public_key_with_invalid_length():
    """
    Case: validate public key with invalid length.
    Expect: length of the public key is not valid error message.
    """
    expected_result = 'Length of the given public key is not valid.'

    with pytest.raises(Exception) as error:
        validate_public_key(public_key='03ba3b69c5f7cf2c0dac39b93dee0d270277115e4926a5355')

    assert expected_result == str(error.value)


def test_validate_public_key_not_in_hexadecimal_string():
    """
    Case: validate public key not in hexadecimal string format.
    Expect: public key is not in hexadecimal string error message.
    """
    expected_result = 'Given public key is not in hexadecimal string format.'
    with pytest.raises(Exception) as error:
        validate_public_key(public_key='03ba3b69c5f7cf2c0dac39b93dee0d270277115e4926a53552813c6abdb07co7xz')

    assert expected_result == str(error.value)
