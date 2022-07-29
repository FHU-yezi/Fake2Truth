from utils.config_manager import config
from typing import Optional


def GenerateURL(uin: int, uid: Optional[int] = None) -> str:
    result = (f"http://{config['target_host']}:{config['external_api_port']}"
              "/card/show_pslcard?version=1&src_type=internal&card_type=group"
              f"&uin={uin}")
    if uid:
        result += f"&uid={uid}"

    return result