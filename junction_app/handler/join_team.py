import json

from sqlalchemy.orm import Session

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
    team = session.query(TeamModel).filter(TeamModel.team_name == team_name).one_or_none()
    if team is None:
        response(404, {"message": "no team"})

    session.add(UserTeamMappingModel(user_id, team.team_id))
    session.commit()

    return response(201)
