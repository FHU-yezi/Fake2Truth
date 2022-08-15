from sanic.response import json


def JSON_404_error():
    return json({
        "code": 404,
        "message": "Page not found"
    })


def JSON_500_error():
    return json({
        "code": 500,
        "message": "Internal server error"
    })


def JSON_502_error():
    return json({
        "code": 502,
        "message": "Bad gateway"
    })
