import json


def response(response_code: int, body=None, header=None) -> dict:
    if header is None:
        header = {}
    if body is None:
        body = {}

    return {
        "statusCode": response_code,
        "body": json.dumps(body),
        "headers": header.update({
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Allow-Methods": "OPTIONS, HEAD, POST, GET, PUT, DELETE",
        }),
    }
