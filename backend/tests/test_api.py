import uuid

import pytest
from wirvsvirus.api import app
from wirvsvirus import models
from wirvsvirus import db
from wirvsvirus.settings import settings

import asyncio
from bson import ObjectId


def test_matches_api(test_client, mock_auth):
    match = models.MatchBase(helper_id=str(ObjectId()), demand_id=str(ObjectId()))
    response = test_client.post('/matches', data=match.json())
    assert response.status_code == 200


def test_hospital_crud_roundtrip(test_client, mock_auth):
    """Test that creating and querying hospitals works."""
    item = models.HospitalBase(name='test', address='test')
    response = test_client.post('/hospitals', data=item.json())
    assert response.status_code == 200
    created_id = response.json()['id']
    query_response = test_client.post('/graphql', json={
        'query': 'query {hospital(id: "HOSPITAL_ID") {name id}}'.replace('HOSPITAL_ID', created_id)
    })
    assert query_response.json() == {'data': {'hospital': {'name': 'test', 'id': created_id}}}



def test_auth(auth_token, test_client):
    """Test authentication validation.

    Skipped if authentication token is missing.
    """
    match = models.MatchBase(helper_id=str(ObjectId()), demand_id=str(ObjectId()))
    m = test_client.post('/matches', data=match.json(), headers={'Authorization': f'Bearer {auth_token}'})
    assert m.status_code == 200
