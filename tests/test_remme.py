"""
Provide tests to Remme client implementation.
"""
import pytest

from remme import Remme


@pytest.mark.asyncio
async def test_create_remme_client():
    """
    Case: create Remme client object.
    Expect: remme object.
    """
    remme = Remme(
            private_key_hex='f4f551c178104595ff184f1786ddb2bfdc74b24562611edcab90d4729fb4bab8',
            network_config={
                'node_address': 'localhost:8080',
                'ssl_mode': False,
            }
        )

    assert isinstance(remme, Remme)


@pytest.mark.asyncio
async def test_create_remme_client_with_invalid_data():
    """
    Case: create Remme client with invalid node_address.
    Expect: error message.
    """
    expected_result = 'You try construct with invalid `node_address`.'

    with pytest.raises(Exception) as error:
        Remme(
            private_key_hex='f4f551c178104595ff184f1786ddb2bfdc74b24562611edcab90d4729fb4bab8',
            network_config={
                'node_address': 'test',
                'ssl_mode': False,
            }
        )

    assert expected_result == str(error.value)
