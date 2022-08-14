from datetime import datetime
from typing import Dict

from httpx import post as httpx_post

from utils.config_manager import config

# TODO：对该模块加入异步支持


def get_feishu_token() -> str:
    """获取飞书 Token

    Raises:
        ValueError: 获取 Token 失败

    Returns:
        str: 飞书 Token
    """
    headers = {"Content-Type": "application/json; charset=utf-8"}
    data = {
        "app_id": config["message_sender/app_id"],
        "app_secret": config["message_sender/app_secret"]
    }
    response = httpx_post("https://open.feishu.cn/open-apis/auth/v3/"
                          "tenant_access_token/internal",
                          headers=headers, json=data)

    if response.json()["code"] == 0:
        return "Bearer " + response.json()["tenant_access_token"]
    else:
        raise ValueError("获取 Token 时发生错误，"
                         f"错误码：{response.json()['code']}，"
                         f"错误信息：{response.json()['msg']}")


def send_feishu_card(card: Dict) -> None:
    """发送飞书卡片

    Args:
        card (Dict): 飞书卡片

    Raises:
        ValueError: 发送飞书卡片失败
    """
    headers = {"Content-Type": "application/json; charset=utf-8",
               "Authorization": get_feishu_token()}
    data = {
        "email": config["message_sender/email"],
        "msg_type": "interactive",
        "card": card
    }
    response = httpx_post("https://open.feishu.cn/open-apis/message/v4/send/",
                          headers=headers, json=data)

    if response.json()["code"] != 0:
        raise ValueError("发送消息卡片时发生错误，"
                         f"错误码：{response.json()['code']}，"
                         f"错误信息：{response.json()['msg']}")


def send_url_accessed_message(access_time: datetime, ip: str, UID: int, user_name: str) -> None:
    card = {
        "header": {
            "template": "green",
            "title": {
                "content": "链接被用户访问",
                "tag": "plain_text"
            }
        },
        "elements": [
            {
                "tag": "div",
                "fields": [
                    {
                        "is_short": True,
                        "text": {
                            "content": f"**访问时间**\n{access_time}",
                            "tag": "lark_md"
                        }
                    },
                    {
                        "is_short": True,
                        "text": {
                            "content": f"**来源 IP**\n{ip}",
                            "tag": "lark_md"
                        }
                    },
                    {
                        "is_short": False,
                        "text": {
                            "content": "\n",
                            "tag": "plain_text"
                        }
                    },
                    {
                        "is_short": True,
                        "text": {
                            "content": f"**用户 ID**\n{UID}",
                            "tag": "lark_md"
                        }
                    },
                    {
                        "is_short": True,
                        "text": {
                            "content": f"**用户名**\n{user_name}",
                            "tag": "lark_md"
                        }
                    }
                ]
            }
        ]
    }

    send_feishu_card(card)
