from utils.datetime_helper import get_now_without_mileseconds
from utils.db_manager import access_log_db
from utils.user_data_manager import get_name_by_UID


async def add_access_log(ip: str, uid: int):
    if uid:
        name = await get_name_by_UID(uid)
    else:
        name = None

    await access_log_db.insert_one({
        "time": get_now_without_mileseconds(),
        "ip": ip,
        "user": {
            "uid": uid,
            "name": name
        }
    })
