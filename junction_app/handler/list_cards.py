from sqlalchemy.orm import Session

from db.card import CardModel
from db.team import TeamModel
from db.user import UserModel
from handler import response, get_user_id_from_header


def lambda_handler(event: dict, context):
    team_name = event.get("queryStringParameters", "{}").get("team_name")
    user_id = event.get("queryStringParameters", "{}").get("user_id")
    progress_status = event.get("queryStringParameters", "{}").get(
        "progress_status")

    if team_name is None and user_id is None:
        return response(400)
    user_id_from_token = get_user_id_from_header(event.get("headers", {}))
    if user_id_from_token is None:
        return response(403)

    session = Session()
    query = session.query(CardModel)
    if team_name is not None:
        team = session.query(TeamModel).filter(
            TeamModel.team_name == team_name).one_or_none()
        if team is None:
            return response(404, {"message": "no team matched"})
        query = query.filter(CardModel.team_id == team.team_id)

    if user_id is not None:
        query = query.filter(CardModel.user_id == user_id)

    if progress_status is not None:
        query = query.filter(CardModel.progress_status == progress_status)

    cards = query.all()

    users = [
        session.query(UserModel).filter(UserModel.user_id == c.user_id).one()
        for c in cards
    ]
    result = [{
        "card_id": card.card_id,
        "goal_focus_minute": card.goal_focus_minute,
        "color": card.color,
        "content": card.content,
        "start_time": card.start_time.isoformat() if card.start_time is not None else None,
        "progress_status": card.progress_status,
        "username": user.username,
    } for user, card in zip(users, cards)]

    return response(200, {"cards": result})
