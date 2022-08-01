from sanic import Blueprint
from sanic.response import json, redirect
from utils.access_log_manager import add_access_log
from utils.validate_helper import can_be_int

card = Blueprint("card", url_prefix="/card")


def get_redirect_url(uin: str, type_: str) -> str:
    if type_ == "user":
        return ("mqqapi://card/show_pslcard?src_type=internal&version=1"
                f"&uin={uin}")
    elif type_ == "group":
        return ("mqqapi://card/show_pslcard?src_type=internal&version=1"
                f"&card_type=group&uin={uin}")
    else:
        raise ValueError()


def validate_pslcard_handler_params(request) -> bool:
    if request.args.get("src_type") != "internal":
        return False
    if request.args.get("version") != "1":
        return False

    if not can_be_int(request.args.get("uin")):
        return False
    if request.args.get("uid") \
       and not can_be_int(request.args.get("uid")):
        return False

    return True


def get_show_pslcard_URL_type(request) -> str:
    if request.args.get("card_type"):
        return "group"
    else:
        return "user"


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
    type_ = get_show_pslcard_URL_type(request)

    await add_access_log(
        type_=type_,
        ip=request.ip,
        uid=uid
    )

    return redirect(get_redirect_url(request.args.get("uin"), type_))
