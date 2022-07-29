from utils.db_manager import user_data_db
from typing import Union


async def IsUIDExists(uid: int) -> bool:
    if await user_data_db.count_documents({"uid": uid}) > 0:
        return True
    return False


async def GetNameByUID(uid: int) -> Union[str, None]:
    if not await IsUIDExists(uid):
        return None

    return await user_data_db.find({"uid": uid})[0]["name"]


async def AddUser(uid: int, name: str):
    user_data_db.insert_one({
        "uid": uid,
        "name": name
    })


async def RemoveUserByUID(uid: int):
    user_data_db.delete_one({
        "uid": uid
    })
