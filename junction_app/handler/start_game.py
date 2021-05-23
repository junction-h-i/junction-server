from datetime import datetime
import json
from typing import List

from sqlalchemy.orm import Session

from db.card import CardModel
from db.team import TeamModel
from db.user_team_mapping import UserTeamMappingModel
from handler import response, get_user_id_from_header


def lambda_handler(event: dict, context):
    team_name = event.get("pathParameters", {}).get("team_name")

    if team_name is None:
        return response(400)

    session = Session()
    team = session.query(TeamModel).filter(
        TeamModel.team_name == team_name
    ).one_or_none()
    if team is None:
        response(404, {"message": "no team"})

    now = datetime.utcnow()
    team.start_time = now
    session.add(team)

    cards: List[CardModel] = session.query(CardModel).filter(
        CardModel.team_id == team.team_id
    ).all()
    for c in cards:
        c.start_time = now
        session.add(c)

    session.commit()

    return response(201)
