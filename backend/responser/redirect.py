from sanic.response import redirect


def redirect_to_QQ_user(uin: int):
    return redirect("mqqapi://card/show_pslcard?src_type=internal&version=1"
                    f"&uin={uin}")


def redirect_to_QQ_group(uin: int):
    return redirect("mqqapi://card/show_pslcard?src_type=internal&version=1"
                    f"&card_type=group&uin={uin}")
