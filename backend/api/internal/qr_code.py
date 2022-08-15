from qrcode import make as qrcode_make
from sanic import Blueprint
from sanic.response import file, json
from utils.url_generator import MAPPING
from utils.user_data_manager import is_UID_exists
from utils.validate_helper import can_be_int

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
    uin = body.get("uin")
    uid = body.get("uid")
    type_ = body.get("type")

    if not validate_get_handler_body(request):
        return json({
            "code": 400,
            "message": "请求参数错误"
        })

    if uid and not await is_UID_exists(uid):
        return json(({
            "code": 400,
            "message": "用户不存在"
        }))

    if type_ not in MAPPING.keys():
        return json({
            "code": 400,
            "message": "链接类型不存在"
        })

    generate_func = MAPPING[type_]
    url = generate_func(uin, uid)
    qr_code = qrcode_make(url)
    # TODO: 清除临时文件
    qr_code.save("qr_code.png", "PNG")

    return await file("qr_code.png")
