from typing import Optional

from qrcode import make as qrcode_make

from gengertor.url_gengertor import generate_group_URL, generate_user_URL

# TODO：定期清理临时文件


def generate_user_QR_code(uin: int, UID: Optional[int] = None) -> str:
    url = generate_user_URL(uin, UID)
    QR_code = qrcode_make(url)
    QR_code.save("qr_code.png", "PNG")
    return "qr_code.png"


def generate_group_QR_code(uin: int, UID: Optional[int] = None) -> str:
    url = generate_group_URL(uin, UID)
    QR_code = qrcode_make(url)
    QR_code.save("qr_code.png", "PNG")
    return "qr_code.png"
