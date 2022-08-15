from typing import Dict, Optional

from utils.datetime_helper import get_now_without_mileseconds
from utils.db_manager import hash_data_db
from utils.hash_helper import get_hash


async def is_hash_exists(hash: str) -> bool:
    if await hash_data_db.count_documents({"_id": hash}) > 0:
        return True
    return False


async def add_hash_data(uin: int, UID: Optional[int], is_one_time: bool) -> str:
    hash = get_hash(12)
    hash_data_db.insert_one({
        "_id": hash,
        "generate_time": get_now_without_mileseconds(),
        "is_one_time": is_one_time,
        "uid": UID,
        "uin": uin
    })
    return hash


async def parse_hash_data(hash: str) -> Dict:
    if not await is_hash_exists(hash):
        raise ValueError("hash 不存在")

    result = await hash_data_db.find_one(
        {"_id": hash},
        {"_id": 0, "uid": 1, "uin": 1}
    )
    return result
