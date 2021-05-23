import json

from sqlalchemy.orm import Session
import jwt

from secret import SECRET_KEY
from db.user import UserModel
from handler import response


def lambda_handler(event: dict, context):
    body = json.loads(event.get("body", "{}"))
    username = body.get("username")
    password = body.get("password")

    if None in [username, password]:
        return response(400)

    session = Session()
    user = session.query(UserModel). \
        filter(UserModel.username == username). \
        filter(UserModel.password == password). \
        one_or_none()

    if user is None:
        return response(400)

    access_token = jwt.encode({"user_id": user.user_id}, SECRET_KEY, algorithm="HS256").decode('utf-8')

    return response(201, {"access_token": access_token})
