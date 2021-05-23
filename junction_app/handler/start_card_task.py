from datetime import datetime

from sqlalchemy.orm import Session

from db.card import CardModel
from db.team import TeamModel
from handler import response, get_user_id_from_header


def lambda_handler(event: dict, context):
    card_id = event.get("pathParameters", {}).get("card_id")
    if card_id is None:
        return response(400)

    user_id = get_user_id_from_header(event.get("headers", {}))
    if user_id is None:
        return response(403)

    session = Session()
    card: CardModel = session.query(CardModel).filter(
        CardModel.card_id == card_id
    ).one_or_none()
    if card is None:
        return response(404, {"message": "wrong card id or user id"})

    team = session.query(TeamModel).filter(
        TeamModel.team_id == card.team_id
    ).one_or_none()
    if team is None:
        response(404, {"message": "no team"})

    card.start_time = datetime.utcnow()
    card.progress_status = "IN_PROGRESS"

    session.add(card)
    session.commit()

    return response(201)
