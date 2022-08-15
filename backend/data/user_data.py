from typing import Dict, List, Union

from utils.db_manager import user_data_db


async def is_UID_exists(uid: int) -> bool:
    if await user_data_db.count_documents({"uid": uid}) > 0:
        return True
    return False


async def get_name_by_UID(uid: int) -> Union[str, None]:
    if not await is_UID_exists(uid):
        return None

    result = await user_data_db.find_one({"uid": uid})
    return result["name"]


async def add_user(uid: int, name: str):
    await user_data_db.insert_one({
        "uid": uid,
        "name": name
    })


async def remove_user_by_UID(uid: int):
    await user_data_db.delete_one({
        "uid": uid
    })


async def get_all_users() -> List[Dict]:
    result = []
    async for item in user_data_db.find(
        {}, {"_id": 0, "uid": 1, "name": 1}
    ).sort("_id", 1):
        result.append(item)
    return result
