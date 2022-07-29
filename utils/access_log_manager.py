from utils.db_manager import access_log_db
from utils.datetime_helper import GetNowWithoutMileseconds
from utils.user_data_manager import GetNameByUID


async def AddAccessLog(ip: str, uid: int):
    if uid:
        name = await GetNameByUID(uid)
    else:
        name = None

    await access_log_db.insert_one({
        "time": GetNowWithoutMileseconds(),
        "ip": ip,
        "user": {
            "uid": uid,
            "name": name
        }
    })
