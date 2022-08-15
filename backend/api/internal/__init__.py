from sanic import Blueprint

from .qr_code import qr_code
from .url import url
from .user import user

internal = Blueprint.group(qr_code, url, user, url_prefix="/internal")
