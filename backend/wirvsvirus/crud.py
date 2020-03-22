"""CRUD utilities."""

from typing import Optional, List
from pydantic import BaseModel
from wirvsvirus import db, models


async def create_item(collection: str, item: BaseModel) -> dict:
    """Simple create item convenience function."""
    result = await db.get_database()[collection].insert_one(item.dict())
    output = await db.get_database()[collection].find_one({'_id': result.inserted_id})
    return output

async def get_item(collection: str, id: str) -> Optional[dict]:
    """Get single item by id."""
    return await db.get_database()[collection].find_one({'_id': id})

async def find(collection: str, query: dict, projection: dict = None) -> List[dict]:
    """Find multiple."""
    documents = []
    async for document in db.get_database()[collection].find(query, projection):
        documents.append(document)
    return documents
