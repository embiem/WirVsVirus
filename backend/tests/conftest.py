#!/usr/bin/env python3

import datetime
import asyncio
from fastapi.testclient import TestClient
import pytest

from wirvsvirus import models, crud
from wirvsvirus.auth import JWTPayload
from wirvsvirus.settings import settings
from bson import ObjectId


@pytest.fixture
def dummy_match():
    return models.MatchBase(
        helper_id=str(ObjectId()),
        personnel_requirement_id=str(ObjectId()),
        start_date=datetime.datetime.utcnow().isoformat(),
        end_date=datetime.datetime.utcnow().isoformat(),
        status="test",
        info_text="stuff",
    )


@pytest.fixture
def dummy_helper():
    return models.Helper(
        first_name="foo",
        last_name="bar",
        email="bla@example.com",
        qualification_id="bla",
        work_experience_in_years=1,
        activity_ids=[],
    )


@pytest.fixture
def dummy_hospital():
    return models.HospitalBase(name="test", address="test")


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
    mock_jwt_payload = JWTPayload(
        **{
            "iss": settings.auth_issuer,
            "sub": "google-oauth2|100000000000000000000",
            "aud": ["wirvsvirus-healthkeeper-api", f"{settings.auth_issuer}userinfo"],
            "iat": 1584810251,
            "exp": 1584896651,
            "azp": "I6FVGpK9w4Uf1efLARivV6B7Umle5Et4",
            "scope": "openid profile email",
        }
    )
    mocker.patch("wirvsvirus.auth.Auth.__call__").return_value = mock_jwt_payload
    return mock_jwt_payload


def _create_model_item(collection, in_item, out_cls):
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(crud.create_item(collection, in_item))
    return out_cls(**result)


@pytest.fixture
def mock_data(db_session):
    hospital = _create_model_item(
        "hospitals", models.HospitalBase(name="test", address="test"), models.Hospital
    )

    helper = _create_model_item(
        "helpers",
        models.HelperBase(
            first_name="foo",
            last_name="bar",
            email="bla@example.com",
            qualification_id="bla",
            work_experience_in_years=1,
            activity_ids=[],
        ),
        models.Helper,
    )

    personnel_requirement = _create_model_item(
        "personnel_requirements",
        {
            **models.PersonnelRequirementBase(hospital_id=hospital.id, activity_id="hotline").dict(), 
        },
        models.PersonnelRequirement,
    )

    match = _create_model_item(
        "matches",
        models.MatchBase(
            helper_id=helper.id,
            personnel_requirement_id=personnel_requirement.id,
            start_date=datetime.datetime.utcnow().isoformat(),
            end_date=datetime.datetime.utcnow().isoformat(),
            status="test",
            info_text="stuff",
        ),
        models.Match,
    )

    return {
        "hospitals": [hospital],
        "helpers": [helper],
        "matches": [match],
        "personnel_requirements": [personnel_requirement],
    }


@pytest.fixture
def mock_hospital_profile(mock_data, mock_auth):
    return _create_model_item(
        "profiles",
        models.ProfileIntermediate(
            user_id=mock_auth.sub,
            email="me@example.com",
            type="Hospital",
            hospital_id=mock_data["hospitals"][0].id,
        ),
        models.Profile,
    )


@pytest.fixture
def mock_helper_profile(mock_data, mock_auth):
    return _create_model_item(
        "profiles",
        models.ProfileIntermediate(
            user_id=mock_auth.sub,
            email="me@example.com",
            type="Helper",
            helper_id=mock_data["helpers"][0].id,
        ),
        models.Profile,
    )
