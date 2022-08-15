from random import choice

CHARS = tuple("0123456789ABCDEFGHIGKLMNOPQRSTUVWXYZ")


def get_hash(length: int) -> str:
    result = [choice(CHARS) for _ in range(length)]
    return "".join(result)
