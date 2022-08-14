def can_be_int(string: str) -> bool:
    try:
        int(string)
    except TypeError:
        return False
    else:
        return True
