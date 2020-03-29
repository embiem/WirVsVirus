
import abc
import logging
from typing import Any, Dict, List, Mapping, Optional, TypeVar, Generic, Sequence, Type

from bson import ObjectId
from bson.errors import InvalidId
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase, AsyncIOMotorCollection
from pydantic import BaseModel, root_validator, validator

from wirvsvirus.settings import settings

logger = logging.getLogger(__name__)

T = TypeVar('T', bound='MongoModel')


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


class ObjectIdStr(str):
    """Field for validate string like ObjectId"""

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if isinstance(v, ObjectId):
            return cls(v)
        else:
            try:
                ObjectId(str(v))
            except InvalidId:
                raise ValueError('Not a valid ObjectId')
            return v


class SnakeCaseModel(BaseModel):

    class Config:
        alias_generator = generate_alias
        allow_population_by_field_name = True


class MongoModel(SnakeCaseModel, Generic[T]):
    """Help class for communicate of Pydantic model and MongoDB"""

    id: ObjectIdStr
    _collection: Optional[str] = None

    @root_validator(pre=True)
    def validate_object_id(cls, v):
        """Validate the mongo object id field."""
        if id_ := v.pop('_id', None):
            v['id'] = id_
        if 'id' not in v:
            v['id'] = ObjectIdStr(ObjectId())
        return v

    def db_dict(self) -> Dict[str, Any]:
        """Generate dictionary for database usage."""
        document = self._replace_object_id_strings(self.dict())
        # use "_id" for mongodb identifier.
        if id_ := document.pop('id', None):
            document['_id'] = id_
        return document

    async def create(self) -> Any:
        id_field = self.__fields__['id']
        if not self.id and not issubclass(id_field.type_, (ObjectId, ObjectIdStr)):
            raise ValueError("Can't convert database generated id.  Must supply id explicitely.")
        result = await self.get_collection().insert_one(self.db_dict())
        self.id = id_field.type_(result.inserted_id)
        return result

    async def update(self):
        db_dict = self.db_dict()
        id = db_dict.pop('_id')
        await self.get_collection().find_one_and_update(
            {'_id': id}, {'$set': db_dict})

    @classmethod
    async def get_by_id(cls: Type[T], id_: Any) -> T:
        id_field = cls.__fields__['id']
        if issubclass(id_field.type_, (ObjectIdStr, ObjectId)):
            id_ = ObjectId(id_)
        document = await cls.get_collection().find_one({"_id": id_})
        if document:
            return cls.parse_obj(document)
        return document

    @classmethod
    def get_collection(cls) -> AsyncIOMotorCollection:
        """Return the database collection instance for this model."""
        if not cls._collection:
            raise ValueError('"_collection" attribute must be set on model class to use a database collection.')
        return get_database()[cls._collection]

    @classmethod
    async def find(cls: Type[T], query: Dict[str, Any]) -> List[T]:
        """Find multiple objects using the query."""
        db_query: Dict[str, Any] = cls._replace_object_id_strings(query)
        results = []
        async for document in cls.get_collection().find(db_query):
            results.append(cls.parse_obj(document))
        return results

    async def delete(self) -> int:
        """Delete record from database and returned the number of deleted items."""
        db_id = self._replace_object_id_strings(self.id)
        if not db_id:
            raise ValueError('Id not set on this object.  Don\'t know what to delete.')
        result = await self.get_collection().delete_one({'_id': db_id})
        return result.deleted_count

    @classmethod
    def _replace_object_id_strings(cls, obj):
        """Replace all nested object id strings with object ids."""
        if isinstance(obj, ObjectIdStr):
            return ObjectId(obj)
        if isinstance(obj, str):
            return obj
        if isinstance(obj, Sequence):
            return [cls._replace_object_id_strings(v) for v in obj]
        if isinstance(obj, Mapping):
            return {k: cls._replace_object_id_strings(v) for k, v in obj.items()}
        return obj
