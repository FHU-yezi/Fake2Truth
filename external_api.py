from sanic import Sanic

from sanic.response import text, redirect, json
from validation import validate_card_query_params
# from access_log_manager import AddAccessLog

external = Sanic("external_api")


@external.route("/card/show_pslcard")
def card(request):
    if not validate_card_query_params(request):
        return json({
            "code": 404,
            "message": "Could not find a existing URL for this request"
        })

    return text(f"yes!{request.args.get('uin')}")


external.run(host="0.0.0.0", port=8080, auto_reload=True)
