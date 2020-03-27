
import abc
import logging
from typing import Optional

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from bson import ObjectId
from bson.errors import InvalidId
from pydantic import BaseModel, root_validator

from wirvsvirus.settings import settings

logger = logging.getLogger(__name__)


class DataBase:
    client: AsyncIOMotorClient = None


db = DataBase()


def get_database() -> AsyncIOMotorDatabase:
    return db.client.get_default_database()


def connect():
    logger.info('connecting to mongo')
    print(settings.db_url)
    db.client = AsyncIOMotorClient(str(settings.db_url))
    logging.info('connected to mongo')


def disconnect():
    logging.info('closing mongodb connection')
    db.client.close()
    logging.info("mongodb connection closed")


def generate_alias(identifier: str):
    """Generate camelcase alias for fields."""
    return ''.join(word.capitalize() if i > 0 else word for i, word in enumerate(identifier.split('_')))


class MongoModel(BaseModel):
    """Help class for communicate of Pydantic model and MongoDB"""


    class Config:
        alias_generator = generate_alias
        allow_population_by_field_name = True

    @root_validator(pre=True)
    def validate_object_id(cls, v):
        """Validate the mongo object id field."""
        if '_id' in v:
            v['id'] = v.pop('_id')
        if 'id' in v:
            if isinstance(v['id'], ObjectId):
                v['id'] = str(v['id'])
            else:
                try:
                    ObjectId(str(v['id']))
                except InvalidId:
                    raise ValueError('"id" field is not a valid ObjectId')
        return v
