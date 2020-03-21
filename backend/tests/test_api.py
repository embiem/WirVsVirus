import uuid

from pytest import fixture
from wirvsvirus.api import Match, app
from wirvsvirus import db
import asyncio


def test_api(test_client):
    match = Match(id=uuid.uuid4(), helper_id=uuid.uuid4(), demand_id=uuid.uuid4())
    m = test_client.post('/matches', data=match.json())
    assert m.status_code == 200
