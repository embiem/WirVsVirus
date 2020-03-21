import uuid

from enum import Enum
from pytest import fixture
from wirvsvirus.api import RoleEnum, CapabilityEnum, HelperModel, MatchModel, app
from wirvsvirus import db
import asyncio


def test_matches(test_client):
    match = MatchModel(id=str(uuid.uuid4()), helper_id=str(uuid.uuid4()), demand_id=str(uuid.uuid4()))
    m = test_client.post('/matches', data=match.json())
    assert m.status_code == 200

def test_helpers(test_client):
    helper1 = HelperModel(id=str(uuid.uuid4()), name="name1", email="mail1@mail.de", address="address1", phone_number="phone_number1", capability=CapabilityEnum("", Enum()), helping_category=RoleEnum("", Enum()))
    helper2 = HelperModel(id=str(uuid.uuid4()), name="name2", email="mail2@mail.de", address="address2", phone_number="phone_number2", capability=CapabilityEnum("", Enum()), helping_category=RoleEnum("", Enum()))
    
    m1 = test_client.post('/helpers', data=helper1.json())
    m2 = test_client.post('/helpers', data=helper2.json())

    assert m1.status_code == m2.status_code == 200
