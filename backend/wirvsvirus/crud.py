"""CRUD utilities."""

from pydantic import BaseModel
from wirvsvirus import db, models


async def create_item(collection: str, item: BaseModel) -> dict:
    """Simple create item convenience function."""
    result = await db.get_database()[collection].insert_one(item.dict())
    output = await db.get_database()[collection].find_one({'_id': result.inserted_id})
    return output
