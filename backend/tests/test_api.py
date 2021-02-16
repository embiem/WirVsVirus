import uuid
import datetime

import pytest
from wirvsvirus.api import app
from wirvsvirus import models, db
from wirvsvirus.settings import settings

import asyncio
from bson import ObjectId


def test_nonexistent_profile(test_client, db_session, mock_auth):
    """Check that a non-existent profile gives the correct response."""
    response = test_client.get("/profile")
    assert (
        response.status_code == 404
    ), f"Expected profile not to exist yet. {response.text}"


def test_auth(auth_token, test_client, db_session):
    """Test authentication validation.

    Skipped if authentication token is missing.
    """
    query_response = test_client.post(
        "/graphql", json={"query": "query {hospitals {name id}}"},
    )
    assert query_response.status_code == 200


def test_hospitals_query(test_client, db_session, mock_auth, mock_data):
    """Test listing of hospitals."""
    query_response = test_client.post(
        "/graphql", json={"query": "query {hospitals {name id}}"},
    )
    assert query_response.json() == {
        "data": {
            "hospitals": [
                {
                    "name": mock_data["hospitals"][0].name,
                    "id": mock_data["hospitals"][0].id,
                }
            ]
        }
    }


def test_create_helper_profile(test_client, db_session, mock_auth):
    """Create a profile of type helper."""
    query_response = test_client.post(
        "/graphql",
        json={
            "query": """
        mutation {
            createHelperProfile (firstName: "foo", lastName: "bar") {
                userId
                type
                helper {
                    email
                }
            }
        }
        """
        },
    )
    actual = query_response.json()
    expected = {
        "data": {
            "createHelperProfile": {
                "userId": mock_auth.sub,
                "type": "Helper",
                "helper": {"email": "me@example.com"},
            }
        }
    }
    assert actual == expected


def test_create_hospital_profile(test_client, db_session, mock_auth, mock_data):
    """Create a profile of type hospital"""
    query_response = test_client.post(
        "/graphql",
        json={
            "query": """
        mutation {
            createHospitalProfile (hospitalId: "__HOSPITAL_ID__") {
                userId
                type
                hospital {
                    name
                }
            }
        }
        """.replace(
                "__HOSPITAL_ID__", mock_data["hospitals"][0].id
            )
        },
    )
    actual = query_response.json()
    expected = {
        "data": {
            "createHospitalProfile": {
                "userId": mock_auth.sub,
                "type": "Hospital",
                "hospital": {"name": mock_data["hospitals"][0].name},
            }
        }
    }
    assert actual == expected


def test_update_helper(
    test_client, db_session, mock_auth, mock_data, mock_helper_profile
):
    """Test that a helper user can update it's helpers info."""
    query_response = test_client.post(
        "/graphql",
        json={
            "query": """
        mutation {
            updateHelper (firstName: "new foo") {
                firstName
                lastName
            }
        }
        """
        },
    )
    actual = query_response.json()
    expected = {"data": {"updateHelper": {"firstName": "new foo", "lastName": "bar"}}}
    assert actual == expected


def test_update_hospital(
    test_client, db_session, mock_auth, mock_data, mock_hospital_profile
):
    """Check that a hospital user can update their hospital."""
    query_response = test_client.post(
        "/graphql",
        json={
            "query": """
        mutation {
            updateHospital (name: "new name") {
                id
                name
            }
        }
        """
        },
    )
    actual = query_response.json()
    expected = {
        "data": {
            "updateHospital": {"id": mock_data["hospitals"][0].id, "name": "new name"},
        }
    }
    assert actual == expected


def test_nested_hospital_query(
    test_client, db_session, mock_auth, mock_data, mock_hospital_profile
):
    """Check that a hospital can be queried."""
    query_response = test_client.post(
        "/graphql",
        json={
            "query": """
        query {
            hospital {
                id
                name
                personnelRequirements {id}
                matches {id helper {id email}}
             }
        }
        """
        },
    )
    actual = query_response.json()
    expected = {
        "data": {
            "hospital": {
                "name": "test",
                "id": mock_data["hospitals"][0].id,
                "personnelRequirements": [
                    {"id": mock_data["personnel_requirements"][0].id}
                ],
                "matches": [
                    {
                        "id": mock_data["matches"][0].id,
                        "helper": {
                            "id": mock_data["helpers"][0].id,
                            "email": mock_data["helpers"][0].email,
                        },
                    }
                ],
            }
        }
    }
    assert actual == expected


def test_nested_helper_query(
    test_client, db_session, mock_auth, mock_data, mock_helper_profile
):
    """Check that a helper can be queried."""
    query_response = test_client.post(
        "/graphql",
        json={
            "query": """
        query {
            helper {
                id
                firstName
                matches {id personnelRequirement {id hospital {name}}}
             }
        }
        """
        },
    )
    actual = query_response.json()
    expected = {
        "data": {
            "helper": {
                "firstName": "foo",
                "id": mock_data["helpers"][0].id,
                "matches": [
                    {
                        "id": mock_data["matches"][0].id,
                        "personnelRequirement": {
                            "id": mock_data["personnel_requirements"][0].id,
                            "hospital": {"name": "test"},
                        },
                    }
                ],
            }
        }
    }
    assert actual == expected


def test_request_helper(test_client, db_session, mock_data, mock_hospital_profile):
    """Test creating a match."""
    query_response = test_client.post(
        "/graphql",
        json={
            "query": """
        mutation {
            requestHelper(helperId: "__HELPER_ID__", personnelRequirementId: "__PR_ID__", infoText: "blabla") {
                personnelRequirement { id }
                helper { firstName }
                status
             }
        }
        """.replace(
                "__PR_ID__", mock_data["personnel_requirements"][0].id
            ).replace(
                "__HELPER_ID__", mock_data["helpers"][0].id
            )
        },
    )
    actual = query_response.json()
    expected = {
        "data": {
            "requestHelper": {
                "personnelRequirement": {"id": mock_data["personnel_requirements"][0].id},
                "helper": {"firstName": mock_data["helpers"][0].first_name},
                "status": "Pending",
            }
        }
    }
    assert actual == expected


def test_update_request(test_client, db_session, mock_data, mock_helper_profile):
    """Test creating a match."""
    query_response = test_client.post(
        "/graphql",
        json={
            "query": """
        mutation {
            updateRequest(matchId: "__MATCH_ID__", status: Accepted) {
                id
                status
                helper { firstName }
                personnelRequirement { id }
             }
        }
        """.replace(
                "__MATCH_ID__", mock_data["matches"][0].id
            )
        },
    )
    actual = query_response.json()
    expected = {
        "data": {
            "updateRequest": {
                "id": mock_data["matches"][0].id,
                "status": "Accepted",
                "personnelRequirement": {
                    "id": mock_data["personnel_requirements"][0].id
                },
                "helper": {"firstName": mock_data["helpers"][0].first_name},
            }
        }
    }
    assert actual == expected


def test_set_personnel_requirement(
    test_client, db_session, mock_data, mock_hospital_profile
):
    """Test creating a match."""
    query_response = test_client.post(
        "/graphql",
        json={
            "query": """
        mutation {
            setPersonnelRequirement(activityId: "activity1", countRequired: 5) {
                activityId
                hospital {
                    personnelRequirements {
                        activityId
                        countRequired
                    }
                }
             }
        }
        """
        },
    )
    actual = query_response.json()
    expected = {
        "data": {
            "setPersonnelRequirement": {
                "activityId": "activity1",
                "hospital": {
                    "personnelRequirements": [
                        {
                            "activityId": mock_data["personnel_requirements"][
                                0
                            ].activity_id,
                            "countRequired": 0,
                        },
                        {"activityId": "activity1", "countRequired": 5},
                    ]
                },
            }
        }
    }
    assert actual == expected

