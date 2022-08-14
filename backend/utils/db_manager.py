from motor.motor_asyncio import AsyncIOMotorClient

from utils.config_manager import config


def init_DB():
    connection: AsyncIOMotorClient = AsyncIOMotorClient(
        config["db_address"],
        config["db_port"]
    )
    db = connection.F2TData
    return db


def GetCollection(name: str):
    return db[name]


db = init_DB()

access_log_db = db.assess_log
user_data_db = db.user_data
