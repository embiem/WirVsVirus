import uuid

import pytest
from wirvsvirus.api import app
from wirvsvirus import models
from wirvsvirus.settings import settings

import asyncio
from bson import ObjectId


def test_profile_api(test_client, db_session, mock_auth):

    response = test_client.get('/profile')
    assert response.status_code == 404, f"Expected profile not to exist yet. {response.text}"

    response = test_client.post('/profile', json={'profileType': 'helper', 'email': 'me@example.com'})
    assert response.status_code == 200
    response_json = response.json()
    assert response_json['userId'] == mock_auth['sub']
    assert response_json['email'] == 'me@example.com'
    assert response_json['profileType'] == 'helper'

    response = test_client.post('/profile', json={'profileType': 'helper', 'email': 'me2@example.com'})
    assert response.status_code == 409


def test_matches_api(test_client, db_session, mock_auth):
    match = models.MatchBase(helper_id=str(ObjectId()), personnel_requirement_id=str(ObjectId()))
    response = test_client.post('/matches', data=match.json())
    assert response.status_code == 200


def test_simple_hospital_crud_roundtrip(test_client, db_session, mock_auth):
    """Test that creating and querying hospitals works."""
    item = models.HospitalBase(name='test', address='test')
    response = test_client.post('/hospitals', data=item.json())
    assert response.status_code == 200
    created_id = response.json()['id']
    query_response = test_client.post('/graphql', json={
        'query': 'query {hospital(id: "HOSPITAL_ID") {name id}}'.replace('HOSPITAL_ID', created_id)
    })
    assert query_response.json() == {'data': {'hospital': {'name': 'test', 'id': created_id}}}


def test_auth(auth_token, test_client, db_session):
    """Test authentication validation.

    Skipped if authentication token is missing.
    """
    match = models.MatchBase(helper_id=str(ObjectId()), personnel_requirement_id=str(ObjectId()))
    m = test_client.post('/matches', data=match.json(), headers={'Authorization': f'Bearer {auth_token}'})
    assert m.status_code == 200

def test_hospitals_graphql(test_client, db_session, mock_auth):
    """Test listing of hospitals."""
    item = models.HospitalBase(name='test', address='test')
    response = test_client.post('/hospitals', data=item.json())
    assert response.status_code == 200
    created_id = response.json()['id']
    query_response = test_client.post('/graphql', json={
        'query': 'query {hospitals {name id}}'.replace('HOSPITAL_ID', created_id)
    })
    assert query_response.json() == {'data': {'hospitals': [{'name': 'test', 'id': created_id}]}}



def test_nested_crud_roundtrip(test_client, db_session, mock_auth):
    """Test that creating and querying hospitals works."""
    item = models.HospitalBase(name='test', address='test')
    response = test_client.post('/hospitals', data=item.json())
    assert response.status_code == 200
    hospital = models.Hospital(**response.json())

    item = models.PersonnelRequirementBase(hospital_id=hospital.id, capability='hotline')
    response = test_client.post('/personnel_requirements', data=item.json())
    assert response.status_code == 200
    personnel_requirement = models.PersonnelRequirement(**response.json())

    query_response = test_client.post('/graphql', json={
        'query': 'query {hospital(id: "HOSPITAL_ID") {name id personnelRequirements {id}}}'.replace('HOSPITAL_ID', hospital.id)
    })
    assert query_response.json() == {
        'data': {
            'hospital': {
                'name': 'test',
                'id': hospital.id,
                'personnelRequirements': [
                    {'id': personnel_requirement.id}
                ]
            }
        }
    }
