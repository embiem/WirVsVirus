import asyncio

import pytest
from pymongo.errors import DuplicateKeyError

from wirvsvirus.db import MongoModel, ObjectIdStr


def run_sync(coroutine):
    """Run async function call synchronously without the need for await."""
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(coroutine)
    return result


def test_mongo_model(db_session):
    class A(MongoModel):
        id: ObjectIdStr = None
        prop: str

        _collection = "test"

    a = A(prop="a")
    initial_id = a.id

    result = run_sync(A.get_by_id(initial_id))
    assert result is None

    # run create and check object is in db
    result = run_sync(a.create())
    assert a.id == initial_id

    a_from_db = run_sync(A.get_by_id(initial_id))
    assert a == a_from_db
    assert a.prop == 'a'

    # second create should raise a duplicate key error
    with pytest.raises(DuplicateKeyError):
        result = run_sync(a.create())

    # run update and check
    a.prop = 'b'
    run_sync(a.update())

    a_from_db = run_sync(A.get_by_id(initial_id))
    assert a == a_from_db
    assert a_from_db.prop == 'b'

    # run delete and check that database no longer has object
    n_deleted = run_sync(a.delete())
    assert n_deleted == 1

    a_from_db = run_sync(A.get_by_id(initial_id))
    assert a_from_db is None

    # run delete again to make sure nothing more is there to delete
    n_deleted = run_sync(a.delete())
    assert n_deleted == 0
