from typing import List
import json

from sqlalchemy.orm import Session

from db.card import CardModel
from db.team import TeamModel
from db.user_team_mapping import UserTeamMappingModel
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

    team = TeamModel(team_name, password, goal_minute)
    session.add(team)
    session.commit()

    cards: List[CardModel] = session.query(CardModel).filter(
        CardModel.user_id == user_id
    ).all()
    for c in cards:
        c.team_id = team.team_id
        session.add(c)

    session.add(UserTeamMappingModel(user_id, team.team_id))
    session.commit()

    return response(201)
