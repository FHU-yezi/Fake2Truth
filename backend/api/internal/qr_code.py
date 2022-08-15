from data.user_data import is_UID_exists
from gengertor.qr_code_generator import (generate_group_QR_code,
                                         generate_user_QR_code)
from sanic import Blueprint
from sanic.response import file, json
from utils.validate_helper import can_be_int

QR_CODE_MAPPING = {
    "user": generate_user_QR_code,
    "group": generate_group_QR_code
}


qr_code = Blueprint("qr_code", url_prefix="/qrcode")


def validate_get_handler_body(request) -> bool:
    if not request.json.get("uin"):
        return False
    if not can_be_int(request.json.get("uin")):
        return False
    if request.json.get("uid") \
       and not can_be_int(request.json.get("uid")):
        return False

    return True


@qr_code.post("/get")
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
        return json(({
            "code": 400,
            "message": "用户不存在"
        }))

    if type_ not in QR_CODE_MAPPING.keys():
        return json({
            "code": 400,
            "message": "二维码类型不存在"
        })

    QR_code = QR_CODE_MAPPING[type_](uin, UID)

    return await file(QR_code)
