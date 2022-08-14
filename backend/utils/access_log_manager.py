from typing import Optional

from utils.datetime_helper import get_now_without_mileseconds
from utils.db_manager import access_log_db


async def add_access_log(type_: str, ip: str, UID: Optional[int], user_name: Optional[str]):
    await access_log_db.insert_one({
        "time": get_now_without_mileseconds(),
        "type": type_,
        "ip": ip,
        "user": {
            "id": UID,
            "name": user_name
        }
    })
