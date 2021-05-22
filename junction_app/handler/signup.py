import json

from sqlalchemy.orm import Session

from handler import response
from db.user import UserModel


def lambda_handler(event: dict, context):
    body = json.loads(event.get("body", "{}"))
    username = body.get("username")
    password = body.get("password")

    if None in [username, password]:
        return response(400)

    session = Session()
    for _ in session.query(UserModel.user_id).filter_by(username=username).all():
        return response(409)

    session.add(UserModel(username, password))
    session.commit()

    return response(201, {"username": username, "pw": password})
