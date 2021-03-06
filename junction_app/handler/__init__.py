import json
from typing import Optional

import jwt

from secret import SECRET_KEY


def response(response_code: int, body=None, header=None) -> dict:
    if header is None:
        header = {}
    if body is None:
        body = {}

    return {
        "statusCode": response_code,
        "body": json.dumps(body),
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Allow-Methods": "OPTIONS, HEAD, POST, GET, PUT, DELETE",
        },
    }


def get_user_id_from_header(headers: dict) -> Optional[int]:
    token = headers.get("Authorization", "").replace("Bearer ", "")

    t = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    return t.get("user_id")
