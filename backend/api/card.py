from sanic import Blueprint
from sanic.response import json, redirect
from utils.access_log_manager import add_access_log
from utils.validate_helper import can_be_int

card = Blueprint("card", url_prefix="/card")


def get_redirect_url(uin: str) -> str:
    return ("mqqapi://card/show_pslcard?src_type=internal&version=1"
            f"&card_type=group&uin={uin}")


def validate_pslcard_handler_params(request) -> bool:
    if request.args.get("src_type") != "internal":
        return False
    if request.args.get("version") != "1":
        return False
    if request.args.get("card_type") != "group":
        return False

    if not can_be_int(request.args.get("uin")):
        return False
    if request.args.get("uid") \
       and not can_be_int(request.args.get("uid")):
        return False

    return True


@card.get("/show_pslcard")
async def show_pslcard_handler(request):
    if not validate_pslcard_handler_params(request):
        # 此处应该返回 400，代表请求参数错误
        # 但为了避免引起怀疑，返回状态码 404
        return json({
            "code": 404,
            "message": "Could not find a existing URL for this request"
        })

    uid = int(request.args.get("uid"))

    await add_access_log(
        ip=request.ip,
        uid=uid
    )

    return redirect(get_redirect_url(request.args.get("uin")))
