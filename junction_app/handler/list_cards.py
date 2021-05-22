from sqlalchemy.orm import Session

from db.card import CardModel
from db.team import TeamModel
from db.user import UserModel
from db.user_team_mapping import UserTeamMappingModel
from handler import response, get_user_id_from_header


def lambda_handler(event: dict, context):
    team_name = event.get("queryStringParameters", "{}").get("team_name")
    user_id = event.get("queryStringParameters", "{}").get("user_id")
    progress_status = event.get("queryStringParameters", "{}").get(
        "progress_status")

    if team_name is None and user_id is None:
        return response(400)
    user_id_from_token = get_user_id_from_header(event.get("headers", {}))
    if user_id_from_token != user_id:
        return response(403)

    session = Session()
    query = session.query(UserModel, CardModel)
    if team_name is not None:
        query = query.join(
            UserTeamMappingModel,
            UserTeamMappingModel.user_id == UserModel.user_id
        ).outerjoin(
            TeamModel, TeamModel.team_id == UserTeamMappingModel.team_id
        ).filter(TeamModel.team_name == team_name)

    if user_id is not None:
        query = query.filter(CardModel.user_id == user_id)

    if progress_status is not None:
        query = query.filter(CardModel.progress_status == progress_status)

    result = [{
        "card_id": card.card_id,
        "goal_focus_minute": card.goal_focus_minute,
        "color": card.color,
        "content": card.content,
        "start_time": card.start_time,
        "progress_status": card.process_status,
        "username": user.username,
    } for card, user in query.all()]

    return response(200, {"cards": result})
