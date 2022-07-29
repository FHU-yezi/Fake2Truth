from sanic import Sanic
from sanic.response import redirect, json
from utils.config_manager import config
from validation import validate_card_query_params

from access_log_manager import AddAccessLog

external = Sanic("external_api")


@external.route("/card/show_pslcard")
async def card(request):
    if not validate_card_query_params(request):
        return json({
            "code": 404,
            "message": "Could not find a existing URL for this request"
        })

    uid = request.args.get("uid")
    await AddAccessLog(
        ip=request.ip,
        uid=uid
    )

    return redirect("mqqapi://card/show_pslcard?src_type=internal&version=1"
                    f"&card_type=group&uin={request.args.get('uin')}")


external.run(host="0.0.0.0", port=config["external_api_port"])
