from typing import Optional

from utils.config_manager import config
from data.hash_data import add_hash_data


async def generate_user_URL(uin: int, UID: Optional[int] = None) -> str:
    hash = await add_hash_data(uin, UID, is_one_time=False)

    result = (f"http://{config['target_host']}:{config['api_service_port']}"
              "/api/card/show_pslcard?version=1&src_type=internal"
              f"&hash={hash}")

    return result


async def generate_group_URL(uin: int, UID: Optional[int] = None) -> str:
    hash = await add_hash_data(uin, UID, is_one_time=False)

    result = (f"http://{config['target_host']}:{config['api_service_port']}"
              "/api/card/show_pslcard?version=1&src_type=internal&card_type=group"
              f"&hash={hash}")

    return result
