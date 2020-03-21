import uuid

import pytest
from wirvsvirus.api import MatchModel, app
from wirvsvirus import db
from wirvsvirus.settings import settings

import asyncio


def test_api(test_client, mock_auth):
    match = MatchModel(id=str(uuid.uuid4()), helper_id=str(uuid.uuid4()), demand_id=str(uuid.uuid4()))
    m = test_client.post('/matches', data=match.json())
    assert m.status_code == 200


def test_auth(auth_token, test_client):
    """Test authentication validation.

    Skipped if authentication token is missing.
    """
    match = MatchModel(id=str(uuid.uuid4()), helper_id=str(uuid.uuid4()), demand_id=str(uuid.uuid4()))
    m = test_client.post('/matches', data=match.json(), headers={'Authorization': f'Bearer {auth_token}'})
    assert m.status_code == 200
