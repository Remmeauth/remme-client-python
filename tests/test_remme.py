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
        account_config={'private_key_hex': 'f4f551c178104595ff184f1786ddb2bfdc74b24562611edcab90d4729fb4bab8'},
        network_config={
            'node_address': 'localhost:8080',
            'ssl_mode': False,
        }
    )

    assert isinstance(remme, Remme)


@pytest.mark.asyncio
async def test_create_remme_client_with_invalid_node_address():
    """
    Case: create Remme client with invalid node address.
    Expect: error message.
    """
    expected_result = 'You try construct with invalid `node_address`, remove protocol and try again.'

    with pytest.raises(Exception) as error:
        Remme(
            account_config={'private_key_hex': 'f4f551c178104595ff184f1786ddb2bfdc74b24562611edcab90d4729fb4bab8'},
            network_config={
                'node_address': 'http://test',
                'ssl_mode': False,
            }
        )

    assert expected_result == str(error.value)


@pytest.mark.asyncio
async def test_create_remme_client_with_invalid_ssl_mode():
    """
    Case: create Remme client with invalid ssl mode.
    Expect: error message.
    """
    expected_result = 'You try construct with invalid `ssl_mode`, `ssl_mode` should has boolean type.'

    with pytest.raises(Exception) as error:
        Remme(
            account_config={'private_key_hex': 'f4f551c178104595ff184f1786ddb2bfdc74b24562611edcab90d4729fb4bab8'},
            network_config={
                'node_address': 'localhost:8080',
                'ssl_mode': 12345,
            }
        )

    assert expected_result == str(error.value)
