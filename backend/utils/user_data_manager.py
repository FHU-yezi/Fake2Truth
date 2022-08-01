from typing import Union

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
    user_data_db.insert_one({
        "uid": uid,
        "name": name
    })


async def remove_user_by_UID(uid: int):
    user_data_db.delete_one({
        "uid": uid
    })
