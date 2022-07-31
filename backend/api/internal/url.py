from sanic import Blueprint
from sanic.response import json
from utils.url_manager import generate_URL
from utils.user_data_manager import is_UID_exists
from utils.validate_helper import can_be_int

url = Blueprint("url", url_prefix="/url")


def validate_get_handler_body(request):
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
    uin = body.get("uin")
    uid = body.get("uid")

    if not validate_get_handler_body(request):
        return json({
            "code": 400,
            "message": "请求参数错误"
        })

    if uid and not await is_UID_exists(uid):
        return json({
            "code": 400,
            "message": "用户不存在"
        })

    url = generate_URL(uin, uid)

    return json({
        "code": 200,
        "message": "操作成功",
        "url": url
    })
