from typing import Dict, List, Union

from utils.db_manager import user_data_db


async def is_UID_exists(UID: int) -> bool:
    if await user_data_db.count_documents({"uid": UID}) > 0:
        return True
    return False


async def get_name_by_UID(UID: int) -> Union[str, None]:
    if not await is_UID_exists(UID):
        raise ValueError("该 UID 不存在")

    result = await user_data_db.find_one({"uid": UID})
    return result["name"]


async def add_user(UID: int, name: str):
    if await is_UID_exists(UID):
        raise ValueError("该 UID 已存在")

    await user_data_db.insert_one({
        "uid": UID,
        "name": name
    })


async def remove_user_by_UID(UID: int):
    if not await is_UID_exists(UID):
        raise ValueError("该 UID 不存在")

    await user_data_db.delete_one({
        "uid": UID
    })


async def get_all_users() -> List[Dict]:
    result = []
    async for item in user_data_db.find(
        {}, {"_id": 0, "uid": 1, "name": 1}
    ).sort("_id", 1):
        result.append(item)
    return result
