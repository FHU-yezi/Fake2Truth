from sanic import Blueprint
from sanic.response import json, redirect
from data.access_log_data import add_access_log
from utils.datetime_helper import get_now_without_mileseconds
from utils.message_sender import send_url_accessed_message
from data.user_data import get_name_by_UID
from utils.validate_helper import can_be_int
from responser.redirect import redirect_to_QQ_group, redirect_to_QQ_user


REDIRECT_MAPPING = {
    "user": redirect_to_QQ_user,
    "group": redirect_to_QQ_group
}


card = Blueprint("card", url_prefix="/card")


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

    UID = int(request.args.get("uid"))
    uin = int(request.args.get("uin"))
    type_ = get_show_pslcard_URL_type(request)
    print(await get_name_by_UID(UID))

    if not UID:
        user_name = None
    else:
        try:
            user_name = await get_name_by_UID(UID)
        except ValueError:  # UID 不存在
            user_name = None

    await add_access_log(
        ip=request.ip,
        UID=UID,
        user_name=user_name
    )

    # TODO：在单独线程中运行消息推送任务
    send_url_accessed_message(
        access_time=get_now_without_mileseconds(),
        ip=request.ip,
        UID=UID,
        user_name=user_name
    )

    redirect_URL = REDIRECT_MAPPING[type_](uin)

    return redirect(redirect_URL)
