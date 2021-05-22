import json

from sqlalchemy.orm import Session

from db.card import CardModel
from handler import response, get_user_id_from_header


def lambda_handler(event: dict, context):
    body = json.loads(event.get("body", "{}"))
    content = body.get("content")
    goal_focus_minute = body.get("goal_focus_minute")
    color = body.get("color")

    if None in [content, goal_focus_minute, color]:
        return response(400)

    user_id = get_user_id_from_header(event.get("headers", {}))
    session = Session()

    session.add(CardModel(user_id, goal_focus_minute, color, content))
    session.commit()

    return response(201)
