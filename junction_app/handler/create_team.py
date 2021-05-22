import json

from sqlalchemy.orm import Session

from db.team import TeamModel
from handler import response, get_user_id_from_header


def lambda_handler(event: dict, context):
    body = json.loads(event.get("body", "{}"))
    team_name = body.get("team_name")
    password = body.get("password")
    goal_minute = body.get("goal_minute")

    if None in [team_name, password, goal_minute]:
        return response(400)

    user_id = get_user_id_from_header(event.get("headers", {}))
    if user_id is None:
        return response(403)

    session = Session()

    session.add(TeamModel(team_name, password, goal_minute))
    session.commit()

    return response(201)
