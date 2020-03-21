#!/usr/bin/env python3

from fastapi.testclient import TestClient
import pytest

from wirvsvirus.settings import settings


@pytest.fixture(scope="session")
def test_client():
    from wirvsvirus.api import app
    from wirvsvirus import db
    import asyncio

    client = TestClient(app)
    asyncio.run(db.connect())

    return client


@pytest.fixture
def auth_token():
    if not settings.auth_token:
        pytest.skip("no auth token given")
    return settings.auth_token


@pytest.fixture
def mock_auth(mocker):
    mock_token_payload = {
        'iss': settings.auth_issuer,
        'sub': 'google-oauth2|106819270537249010245',
        'aud': ['wirvsvirus-healthkeeper-api', f'{settings.auth_issuer}userinfo'],
        'iat': 1584810251, 'exp': 1584896651, 'azp': 'I6FVGpK9w4Uf1efLARivV6B7Umle5Et4',
        'scope': 'openid profile email'
    }
    mocker.patch('wirvsvirus.auth.Auth.__call__').return_value = mock_token_payload
    return mock_token_payload
