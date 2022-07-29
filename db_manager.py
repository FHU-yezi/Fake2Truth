from motor import MotorClient

from config_manager import config


def InitDB():
    connection: MotorClient = MotorClient(config["db_address"],
                                          config["db_port"])
    db = connection.F2TData
    return db


def GetCollection(name: str):
    return db[name]


db = InitDB()

run_log_db = db.run_log
access_log_db = db.assess_log
