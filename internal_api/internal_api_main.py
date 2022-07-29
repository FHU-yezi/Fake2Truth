from qrcode import make as qrcode_make
from sanic import Sanic
from sanic.response import file, json
from utils.config_manager import config
from utils.user_data_manager import AddUser, IsUIDExists, RemoveUserByUID

from url_generator import GenerateURL

internal = Sanic("internal_api")


@internal.post("/AddUser")
async def AddUserAPI(request):
    body = request.json
    uid = body.get("uid")
    name = body.get("name")

    if not uid or not name:
        return json({
            "code": 400,
            "message": "请求参数错误"
        })

    try:
        uid = int(uid)
    except ValueError:
        return json({
            "code": 400,
            "message": "请求参数错误"
        })

    if await IsUIDExists(uid):
        return json({
            "code": 400,
            "message": "该用户已存在"
        })

    await AddUser(uid, name)
    return json({
        "code": 200,
        "message": "操作成功"
    })


@internal.post("/RemoveUser")
async def RemoveUserAPI(request):
    body = request.json
    uid = body.get("uid")

    if not uid:
        return json({
            "code": 400,
            "message": "请求参数错误"
        })

    if not await IsUIDExists(uid):
        return json({
            "code": 400,
            "message": "用户不存在"
        })

    await RemoveUserByUID(uid)
    return json({
        "code": 200,
        "message": "操作成功"
    })


@internal.post("/GetURL")
async def GetURLAPI(request):
    body = request.json
    uin = body.get("uin")
    uid = body.get("uid")

    if not uin:
        return json({
            "code": 400,
            "message": "请求参数错误"
        })

    try:
        if uid:
            int(uid)
        int(uin)
    except ValueError:
        return json({
            "code": 400,
            "message": "请求参数错误"
        })

    if uid and not await IsUIDExists(uid):
        return json({
            "code": 400,
            "message": "用户不存在"
        })

    return json({
        "code": 200,
        "message": "操作成功",
        "url": GenerateURL(uin, uid)
    })


@internal.post("/GetQRCode")
async def GetQRCodeAPI(request):
    body = request.json
    uin = body.get("uin")
    uid = body.get("uid")

    if not uin:
        return json({
            "code": 400,
            "message": "请求参数错误"
        })

    try:
        if uid:
            int(uid)
        int(uin)
    except ValueError:
        return json({
            "code": 400,
            "message": "请求参数错误"
        })

    if uid and not await IsUIDExists(uid):
        return json({
            "code": 400,
            "message": "用户不存在"
        })

    url = GenerateURL(uin, uid)
    qr_code = qrcode_make(url)
    # TODO: 清除临时文件
    qr_code.save("qr_code.png", "PNG")
    return await file("qr_code.png")


internal.run(host="0.0.0.0", port=config["internal_api_port"], access_log=False)
