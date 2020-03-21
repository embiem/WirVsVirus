#!/usr/bin/env python3

from fastapi.testclient import TestClient
import pytest


@pytest.fixture(scope="session")
def test_client():
    from wirvsvirus.api import app
    from wirvsvirus import db
    import asyncio

    client = TestClient(app)
    asyncio.run(db.connect())

    return client

