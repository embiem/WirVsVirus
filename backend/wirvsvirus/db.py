import logging

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from wirvsvirus.settings import settings

logger = logging.getLogger(__name__)


class DataBase:
    client: AsyncIOMotorClient = None


db = DataBase()


async def get_database() -> AsyncIOMotorDatabase:
    return db.client[settings.db_db]


async def connect():
    logger.info('connecting to mongo')
    db.client = AsyncIOMotorClient(str(settings.db_url),)
    logging.info('connected to mongo')


async def disconnect():
    logging.info('closing mongodb connection')
    db.client.close()
    logging.info("mongodb connection closed")
