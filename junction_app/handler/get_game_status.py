from sqlalchemy.orm import Session

from db.card import CardModel
from db.team import TeamModel
from db.user import UserModel
from db.user_team_mapping import UserTeamMappingModel
from handler import response, get_user_id_from_header


def lambda_handler(event: dict, context):
    team_name = event.get("queryStringParameters", "{}").get("team_name")

    user_id = get_user_id_from_header(event.get("headers", {}))
    if user_id is None:
        return response(403)

    session = Session()

    team = session.query(TeamModel).filter(TeamModel.team_name == team_name).one_or_none()
    if team is None:
        return response(404, {"message": "wrong team name"})

    users = session.query(UserModel).join(
        UserTeamMappingModel, UserTeamMappingModel.team_id == team.team_id
    )

    for user in users:
        if user.user_id == user_id:
            break
    else:
        return response(403)

    my_cards = session.query(CardModel).filter(CardModel.user_id == user_id).all()
    my_count = {
        "count": len(my_cards),
        "done_count": len([c for c in my_cards if c.process_status == "DONE"])
    }

    team_cards = session.query(CardModel).filter(
        CardModel.team_id == team.team_id).all()
    team_count = {
        "count": len(team_cards),
        "done_count": len([c for c in team_cards if c.process_status == "DONE"])
    }

    return response(200, {
        "team_name": team.team_name,
        "start_time": team.start_time,
        "user_names": [user.username for user in users],
        "all_cards": team_count,
        "my_cards": my_count
    })
