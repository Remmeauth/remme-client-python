"""
Provide tests to implement certificate creation.
"""
import pytest
from datetime import datetime

from cryptography import x509

from remme import Remme

remme = Remme(account_config={'private_key_hex': 'f4f551c178104595ff184f1786ddb2bfdc74b24562611edcab90d4729fb4bab8'})


@pytest.mark.asyncio
async def test_create_certificate():
    """
    Case: create certificate by given data.
    Expect: certificate object with type x509.Certificate.
    """
    certificate = remme.certificate.create({
        'common_name': 'user_name',
        'email': 'user@email.com',
        'name': 'John',
        'surname': 'Smith',
        'country_name': 'US',
        'validity': 360,
        'serial': str(datetime.now()),
    })

    assert isinstance(certificate, x509.Certificate)
