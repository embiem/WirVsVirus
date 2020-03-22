import uuid
import datetime

import pytest
from wirvsvirus.api import app
from wirvsvirus import models, db
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

dummy_helper = models.HelperBase(
    first_name='foo', last_name='bar',
    email='bla@example.com', qualification_id='bla',
    work_experience_in_years=1,
    activity_ids=[])

dummy_hospital = models.HospitalBase(name='test', address='test')

def test_nonexistent_profile(test_client, db_session, mock_auth):
    """Check that a non-existent profile gives the correct response."""
    response = test_client.get('/profile')
    assert response.status_code == 404, f"Expected profile not to exist yet. {response.text}"


def test_hospital_profile(test_client, db_session, mock_auth):
    """Test a hospital profile workflow."""
    base_hospital_profile = {'profileType': 'hospital', 'email': 'me@example.com'}

    # make sure that profile with missing data isn't accepted
    response = test_client.post('/profile', json=base_hospital_profile)
    assert response.status_code == 400, 'we are missing our hospital profile here'

    # make sure that profile with missing hospital isn't accepted
    nonexistent_hospital_profile = {**base_hospital_profile, 'hospital_id': str(ObjectId())}
    response = test_client.post('/profile', json=nonexistent_hospital_profile)
    assert response.status_code == 404

    # try the same for a hospital endpoint (create the hospital first)
    response = test_client.post('/hospitals', data=dummy_hospital.json())
    assert response.status_code == 200
    hospital_id = response.json()['id']
    hospital_profile = {**base_hospital_profile, 'hospitalId': hospital_id}
    response = test_client.post('/profile', json=hospital_profile)
    assert response.status_code == 200
    response_json = response.json()
    assert response_json['userId'] == mock_auth['sub']
    assert response_json['email'] == 'me@example.com'
    assert response_json['profileType'] == 'hospital'
    assert response_json.get('helperId') is None, 'No helper id expected for hospital profile'
    assert response_json['hospitalId'] == hospital_id, 'expected hospital id to be present'

    # make sure we can't repose once a profile is created
    response = test_client.post('/profile', json=hospital_profile)
    assert response.status_code == 409


def test_helper_profile(test_client, db_session, mock_auth):
    """Test a helper profile workflow."""
    base_helper_profile = {'profileType': 'helper', 'email': 'me@example.com'}

    # post incomplete profiles
    response = test_client.post('/profile', json=base_helper_profile)
    assert response.status_code == 400, 'we are missing our helper profile here'

    # now lets try and post working profiles
    helper_profile = {**base_helper_profile, 'helper': dummy_helper.dict()}
    response = test_client.post('/profile', json=helper_profile)
    assert response.status_code == 200
    response_json = response.json()
    assert response_json['userId'] == mock_auth['sub']
    assert response_json['email'] == 'me@example.com'
    assert response_json['profileType'] == 'helper'
    assert response_json['helperId'], 'expected helper id to be present'

    # make sure we can't repose once a profile is created
    response = test_client.post('/profile', json=helper_profile)
    assert response.status_code == 409

def test_create_match(test_client, db_session, mock_auth):
    """Test creating a match."""
    response = test_client.post('/matches', data=dummy_match.json())
    assert response.status_code == 200


def test_simple_hospital_crud_roundtrip(test_client, db_session, mock_auth):
    """Test that creating and querying hospitals works."""
    response = test_client.post('/hospitals', data=dummy_hospital.json())
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

def test_hospitals_graphql_roundtrip(test_client, db_session, mock_auth):
    """Test listing of hospitals."""
    item = models.HospitalBase(name='test', address='test')
    response = test_client.post('/hospitals', data=item.json())
    assert response.status_code == 200
    created_id = response.json()['id']
    query_response = test_client.post('/graphql', json={
        'query': 'query {hospitals {name id}}'.replace('HOSPITAL_ID', created_id)
    })
    assert query_response.json() == {'data': {'hospitals': [{'name': 'test', 'id': created_id}]}}



def test_nested_hospitals_crud_roundtrip(test_client, db_session, mock_auth):
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
