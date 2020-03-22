#!/usr/bin/env python3

from fastapi.testclient import TestClient
import pytest

from wirvsvirus.settings import settings


@pytest.fixture(scope="session")
def db():
    from wirvsvirus import db
    db.connect()
    return db


@pytest.fixture(scope="session")
def test_client():
    from wirvsvirus.api import app
    # for testing we always want this to be enabled.
    # If we need to disable it, we will do so in fixtures
    settings.auth_enabled = True

    client = TestClient(app)
    return client

@pytest.fixture
def db_session(db):
    db.db.client.drop_database(db.get_database())
    return db

@pytest.fixture
def auth_token():
    if not settings.auth_token:
        pytest.skip("no auth token given")
    return settings.auth_token

@pytest.fixture
def mock_auth(mocker):
    mock_token_payload = {
        'iss': settings.auth_issuer,
        'sub': 'google-oauth2|100000000000000000000',
        'aud': ['wirvsvirus-healthkeeper-api', f'{settings.auth_issuer}userinfo'],
        'iat': 1584810251, 'exp': 1584896651, 'azp': 'I6FVGpK9w4Uf1efLARivV6B7Umle5Et4',
        'scope': 'openid profile email'
    }
    mocker.patch('wirvsvirus.auth.Auth.__call__').return_value = mock_token_payload
    return mock_token_payload
