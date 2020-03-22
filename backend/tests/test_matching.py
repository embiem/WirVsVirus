"""Test matching algorithm."""

from wirvsvirus.matching import MatchingModel

example_problem = {
    "hospitals": [
        {
            "name": "Hospital Cologne",
            "latitude": 50.9,
            "longitude": 6.9,
            "demand": {"admin": 1, "medical": 4, "logistic": 3},
        },
        {
            "name": "Hospital Berlin",
            "latitude": 52.5,
            "longitude": 13.4,
            "demand": {"admin": 0, "medical": 2, "logistic": 0},
        },
        {
            "name": "Hospital Frankfurt",
            "latitude": 50.1,
            "longitude": 8.7,
            "demand": {"admin": 0, "medical": 10, "logistic": 1},
        },
    ],
    "worker": [
        {
            "name": "Student Göttingen",
            "skill": "medical",
            "latitude": 51.45,
            "longitude": 9.9,
        },
        {
            "name": "Student Wuppertal",
            "skill": "medical",
            "latitude": 51.2,
            "longitude": 7.15,
        },
        {
            "name": "Student Fulda",
            "skill": "medical",
            "latitude": 50.6,
            "longitude": 9.7,
        },
        {
            "name": "Student Luckenwalde",
            "skill": "medical",
            "latitude": 52.1,
            "longitude": 13.2,
        },
        {
            "name": "Student Windischletten",
            "skill": "medical",
            "latitude": 50,
            "longitude": 11,
        },
        {
            "name": "Student Baden-Baden",
            "skill": "medical",
            "latitude": 48.8,
            "longitude": 8.2,
        },
        {
            "name": "Student Koblenz",
            "skill": "medical",
            "latitude": 50.4,
            "longitude": 7.6,
        },
        {
            "name": "Admin Koblenz",
            "skill": "admin",
            "latitude": 50.4,
            "longitude": 7.6,
        },
        {
            "name": "Admin Wuppertal",
            "skill": "admin",
            "latitude": 51.2,
            "longitude": 7.15,
        },
        {
            "name": "Logistic Göttingen",
            "skill": "logistic",
            "latitude": 51.45,
            "longitude": 9.9,
        },
        {
            "name": "Logistic Wuppertal",
            "skill": "logistic",
            "latitude": 51.2,
            "longitude": 7.15,
        },
        {
            "name": "Logistic Fulda",
            "skill": "logistic",
            "latitude": 50.6,
            "longitude": 9.7,
        },
        {
            "name": "Logistic Luckenwalde",
            "skill": "logistic",
            "latitude": 52.1,
            "longitude": 13.2,
        },
        {
            "name": "Logistic Windischletten",
            "skill": "logistic",
            "latitude": 50,
            "longitude": 11,
        },
    ],
}


def test_matching():
    """Test matching example."""
    model = MatchingModel(example_problem)
    model.solve()
    results = model.results
    assert results == {
        "objective": 1033.0,
        "allocation": {
            "Hospital Cologne": [
                "Student Wuppertal",
                "Student Koblenz",
                "Admin Wuppertal",
                "Logistic Göttingen",
                "Logistic Wuppertal",
                "Logistic Fulda",
            ],
            "Hospital Berlin": ["Student Luckenwalde"],
            "Hospital Frankfurt": [
                "Student Göttingen",
                "Student Fulda",
                "Student Windischletten",
                "Student Baden-Baden",
                "Logistic Windischletten",
            ],
        },
    }
