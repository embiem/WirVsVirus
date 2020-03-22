import uuid
import datetime

import pytest
from wirvsvirus.api import app
from wirvsvirus import models
from wirvsvirus.settings import settings

import asyncio
from bson import ObjectId


dummy_match = models.MatchBase(
        helper_id=str(ObjectId()),
        personnel_requirement_id=str(ObjectId()),
        start_date=datetime.datetime.utcnow().isoformat(),
        end_date=datetime.datetime.utcnow().isoformat(),
        status='test',
        info_text='stuff'
    )


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
    response = test_client.post('/matches', data=dummy_match.json())
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
    m = test_client.post('/matches', data=dummy_match.json(), headers={'Authorization': f'Bearer {auth_token}'})
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

    item = models.PersonnelRequirementBase(hospital_id=hospital.id, activity_id='hotline')
    response = test_client.post('/personnel_requirements', data=item.json())
    assert response.status_code == 200
    personnel_requirement = models.PersonnelRequirement(**response.json())

    item = models.HelperBase(first_name='foo', last_name='bar',
                             email='bla@example.com', qualification_id='bla',
                             work_experience_in_years=1,
                             activity_ids=[])
    response = test_client.post('/helpers', data=item.json())
    assert response.status_code == 200
    helper = models.Helper(**response.json())

    item = dummy_match.copy()
    item.personnel_requirement_id = personnel_requirement.id
    item.helper_id = helper.id

    response = test_client.post('/matches', data=item.json())
    assert response.status_code == 200
    match = models.Match(**response.json())

    query_response = test_client.post('/graphql', json={
        'query': '''
        query {
            hospital(id: "HOSPITAL_ID") {
                id
                name
                personnelRequirements {id}
                matches {id helper {id email}}
             }
        }
        '''.replace('HOSPITAL_ID', hospital.id)
    })
    assert query_response.json() == {
        'data': {
            'hospital': {
                'name': 'test',
                'id': hospital.id,
                'personnelRequirements': [
                    {'id': personnel_requirement.id}
                ],
                'matches': [
                    {
                        'id': match.id,
                        'helper': {
                            'id': helper.id,
                            'email': helper.email
                        }
                    }
                ]
            }
        }
    }
