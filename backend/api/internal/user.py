from sanic import Blueprint
from sanic.response import json
from utils.user_data_manager import add_user, is_UID_exists, remove_user_by_UID
from utils.validate_helper import can_be_int

user = Blueprint("user", url_prefix="/user")


def validate_add_handler_body(request) -> bool:
    if not request.json.get("uid"):
        return False
    if not request.json.get("name"):
        return False
    if not can_be_int(request.json.get("uid")):
        return False

    return True


def validate_remove_handler_body(request) -> bool:
    if not request.json.get("uid"):
        return False
    if not can_be_int(request.json.get("uid")):
        return False

    return True


@user.post("/add")
async def add_handler(request):
    body = request.json
    uid = body.get("uid")
    name = body.get("name")

    if not validate_add_handler_body(request):
        return json({
            "code": 400,
            "message": "请求参数错误"
        })

    if await is_UID_exists(uid):
        return json({
            "code": 400,
            "message": "该用户已存在"
        })

    await add_user(uid, name)

    return json({
        "code": 200,
        "message": "操作成功"
    })


@user.post("/remove")
async def remove_handler(request):
    body = request.json
    uid = body.get("uid")

    if not validate_remove_handler_body(request):
        return json({
            "code": 400,
            "message": "请求参数错误"
        })

    if not await is_UID_exists(uid):
        return json({
            "code": 400,
            "message": "用户不存在"
        })

    await remove_user_by_UID(uid)

    return json({
        "code": 200,
        "message": "操作成功"
    })
