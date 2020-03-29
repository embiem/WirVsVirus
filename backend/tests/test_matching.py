"""Test matching algorithm."""

from wirvsvirus.matching import MatchingModel
from wirvsvirus.models import (
    Helper,
    Hospital,
    Location,
    PersonnelRequirement,
)

example_problem = {
    "hospitals": [
        {
            "name": "Hospital Cologne",
            "_id": "Hospital Cologne",
            "location": {"type": "Point", "coordinates": [50.9, 6.9]},
            "latitude": 50.9,
            "longitude": 6.9,
            "demand": {"admin": 1, "medical": 4, "logistic": 3},
        },
        {
            "name": "Hospital Berlin",
            "_id": "Hospital Berlin",
            "location": {"type": "Point", "coordinates": [52.5, 13.4]},
            "latitude": 52.5,
            "longitude": 13.4,
            "demand": {"admin": 0, "medical": 2, "logistic": 0},
        },
        {
            "name": "Hospital Frankfurt",
            "_id": "Hospital Frankfurt",
            "location": {"type": "Point", "coordinates": [50.1, 8.7]},
            "latitude": 50.1,
            "longitude": 8.7,
            "demand": {"admin": 0, "medical": 10, "logistic": 1},
        },
    ],
    "worker": [
        {
            "name": "Student Göttingen",
            "_id": "1",
            "activity_ids": ["medical"],
            "location": {"type": "Point", "coordinates": [51.45, 9.9]},
            "latitude": 51.45,
            "longitude": 9.9,
        },
        {
            "name": "Student Wuppertal",
            "_id": "2",
            "activity_ids": ["medical"],
            "location": {"type": "Point", "coordinates": [51.2, 7.15]},
            "latitude": 51.2,
            "longitude": 7.15,
        },
        {
            "name": "Student Fulda",
            "_id": "3",
            "activity_ids": ["medical"],
            "location": {"type": "Point", "coordinates": [50.6, 9.7]},
            "latitude": 50.6,
            "longitude": 9.7,
        },
        {
            "name": "Student Luckenwalde",
            "_id": "4",
            "activity_ids": ["medical"],
            "location": {"type": "Point", "coordinates": [52.1, 13.2]},
            "latitude": 52.1,
            "longitude": 13.2,
        },
        {
            "name": "Student Windischletten",
            "_id": "5",
            "activity_ids": ["medical"],
            "location": {"type": "Point", "coordinates": [50, 11]},
            "latitude": 50,
            "longitude": 11,
        },
        {
            "name": "Student Baden-Baden",
            "_id": "6",
            "activity_ids": ["medical"],
            "location": {"type": "Point", "coordinates": [48.8, 8.2]},
            "latitude": 48.8,
            "longitude": 8.2,
        },
        {
            "name": "Student Koblenz",
            "_id": "7",
            "activity_ids": ["medical"],
            "location": {"type": "Point", "coordinates": [50.4, 7.6]},
            "latitude": 50.4,
            "longitude": 7.6,
        },
        {
            "name": "Admin Koblenz",
            "_id": "8",
            "activity_ids": ["admin"],
            "location": {"type": "Point", "coordinates": [50.4, 7.6]},
            "latitude": 50.4,
            "longitude": 7.6,
        },
        {
            "name": "Admin Wuppertal",
            "_id": "9",
            "activity_ids": ["admin"],
            "location": {"type": "Point", "coordinates": [51.2, 7.15]},
            "latitude": 51.2,
            "longitude": 7.15,
        },
        {
            "name": "Logistic Göttingen",
            "_id": "10",
            "activity_ids": ["logistic"],
            "location": {"type": "Point", "coordinates": [51.45, 9.9]},
            "latitude": 51.45,
            "longitude": 9.9,
        },
        {
            "name": "Logistic Wuppertal",
            "_id": "11",
            "activity_ids": ["logistic"],
            "location": {"type": "Point", "coordinates": [51.2, 7.15]},
            "latitude": 51.2,
            "longitude": 7.15,
        },
        {
            "name": "Logistic Fulda",
            "_id": "12",
            "activity_ids": ["logistic"],
            "location": {"type": "Point", "coordinates": [50.6, 9.7]},
            "latitude": 50.6,
            "longitude": 9.7,
        },
        {
            "name": "Logistic Luckenwalde",
            "_id": "13",
            "activity_ids": ["logistic"],
            "location": {"type": "Point", "coordinates": [52.1, 13.2]},
            "latitude": 52.1,
            "longitude": 13.2,
        },
        {
            "name": "Logistic Windischletten",
            "_id": "14",
            "activity_ids": ["logistic"],
            "location": {"type": "Point", "coordinates": [50, 11]},
            "latitude": 50,
            "longitude": 11,
        },
    ],
}


def test_matching():
    """Test matching example."""
    model = MatchingModel(
        hospitals=example_problem["hospitals"], worker=example_problem["worker"]
    )
    model.solve()
    results = model.results
    assert results == {
        "objective": 1033.0,
        "allocations": [
            {
                "hospital_id": "Hospital Cologne",
                "helper_ids": ["2", "7", "9", "10", "11", "12"],
            },
            {"hospital_id": "Hospital Berlin", "helper_ids": ["4"]},
            {
                "hospital_id": "Hospital Frankfurt",
                "helper_ids": ["1", "3", "5", "6", "14"],
            },
        ],
    }


def test_propose_matching_endpoint(test_client, db_session, mock_auth):
    """Test propose matching endpoint."""

    def fill_db():
        """Fill database with example problem data."""
        for h in example_problem["hospitals"]:
            hospital = Hospital(
                name=h["name"],
                address="",
                location=Location(
                    type="Point", coordinates=(h["latitude"], h["longitude"])
                ),
            )
            response = test_client.post("/hospitals", data=hospital.json())
            response.raise_for_status()
            hospital_id = response.json()["id"]
            for activity, value in h["demand"].items():
                requirement = PersonnelRequirement(
                    hospital_id=hospital_id, activity_id=activity, value=value
                )
                response = test_client.post(
                    "/personnel_requirements", data=requirement.json()
                )
                response.raise_for_status()
        for w in example_problem["worker"]:
            helper = Helper(
                first_name=w["name"].split(" ")[0],
                last_name=w["name"].split(" ")[1],
                email="",
                phone="",
                location=Location(
                    type="Point", coordinates=(w["latitude"], w["longitude"])
                ),
                qualification_id="",
                work_experience_in_years=1,
                activity_ids=w["activity_ids"],
            )
            response = test_client.post("/helpers", data=helper.json())
            response.raise_for_status()

    fill_db()
    response = test_client.get("/matches/propositions")
    assert response.status_code == 200
    response = response.json()
    assert "allocations" in response
    assert "hospitalId" in response["allocations"][0]
    assert "helperIds" in response["allocations"][0]
