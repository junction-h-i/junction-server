import json
from typing import List

from sqlalchemy.orm import Session

from db.card import CardModel
from db.team import TeamModel
from db.user_team_mapping import UserTeamMappingModel
from handler import response, get_user_id_from_header


def lambda_handler(event: dict, context):
    team_name = event.get("pathParameters", {}).get("team_name")
    body = json.loads(event.get("body", "{}"))
    password = body.get("password")

    if None in [team_name, password]:
        return response(400)

    user_id = get_user_id_from_header(event.get("headers", {}))
    if user_id is None:
        return response(403)

    session = Session()
    team = session.query(TeamModel).filter(
        TeamModel.team_name == team_name
    ).one_or_none()
    if team is None:
        response(404, {"message": "no team"})

    cards: List[CardModel] = session.query(CardModel).filter(
        CardModel.user_id == user_id
    ).all()
    for c in cards:
        c.team_id = team.team_id
        session.add(c)

    session.add(UserTeamMappingModel(user_id, team.team_id))
    session.commit()

    return response(201)
