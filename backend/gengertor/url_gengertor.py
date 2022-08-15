from typing import Optional

from utils.config_manager import config


def generate_user_URL(uin: int, UID: Optional[int] = None) -> str:
    result = (f"http://{config['target_host']}:{config['api_service_port']}"
              "/api/card/show_pslcard?version=1&src_type=internal"
              f"&uin={uin}")
    if UID:
        result += f"&uid={UID}"

    return result


def generate_group_URL(uin: int, UID: Optional[int] = None) -> str:
    result = (f"http://{config['target_host']}:{config['api_service_port']}"
              "/api/card/show_pslcard?version=1&src_type=internal&card_type=group"
              f"&uin={uin}")
    if UID:
        result += f"&uid={UID}"

    return result
