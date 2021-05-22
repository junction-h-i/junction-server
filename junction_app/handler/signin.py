from handler import response
import json


def lambda_handler(event: dict, context):
    body = json.loads(event.get("body", "{}"))
    username = body.get("username")
    password = body.get("password")

    if None in [username, password]:
        return response(400)

    return response(201, {"username": username, "pw": password})
