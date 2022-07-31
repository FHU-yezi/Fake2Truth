from sanic import Blueprint

from .card import card
from .internal import internal

api = Blueprint.group(card, internal, url_prefix="/api")
