from data.user_data import is_UID_exists
from gengertor.url_gengertor import generate_group_URL, generate_user_URL
from sanic import Blueprint
from sanic.response import json
from utils.validate_helper import can_be_int

URL_MAPPING = {
    "user": generate_user_URL,
    "group": generate_group_URL
}


url = Blueprint("url", url_prefix="/url")


def validate_get_handler_body(request) -> bool:
    if not request.json.get("uin"):
        return False
    if not can_be_int(request.json.get("uin")):
        return False
    if request.json.get("uid") \
       and not can_be_int(request.json.get("uid")):
        return False

    return True


@url.post("/get")
async def get_handler(request):
    body = request.json
    uin = int(body.get("uin"))
    UID = int(body.get("uid"))
    type_ = body.get("type")

    if not validate_get_handler_body(request):
        return json({
            "code": 400,
            "message": "请求参数错误"
        })

    if UID and not await is_UID_exists(UID):
        return json({
            "code": 400,
            "message": "用户不存在"
        })

    if type_ not in URL_MAPPING.keys():
        return json({
            "code": 400,
            "message": "链接类型不存在"
        })

    generate_func = URL_MAPPING[type_]
    url = generate_func(uin, UID)

    return json({
        "code": 200,
        "message": "操作成功",
        "url": url
    })
