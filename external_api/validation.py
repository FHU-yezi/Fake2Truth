def validate_card_query_params(request) -> bool:
    if request.args.get("src_type") != "internal":
        return False
    if request.args.get("version") != "1":
        return False
    if request.args.get("card_type") != "group":
        return False

    try:
        int(request.args.get("uin"))
    except ValueError:  # 不是 int 类型
        return False

    return True
