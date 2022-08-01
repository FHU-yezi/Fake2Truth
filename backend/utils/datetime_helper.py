from datetime import datetime


def get_now_without_mileseconds() -> datetime:
    return datetime.now().replace(microsecond=0)
