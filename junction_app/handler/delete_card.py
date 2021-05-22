from sqlalchemy.orm import Session

from db.card import CardModel
from handler import response, get_user_id_from_header


def lambda_handler(event: dict, context):
    card_id = event.get("pathParameters", "{}").get("card_id")
    if None in [card_id]:
        return response(400)

    user_id = get_user_id_from_header(event.get("headers", {}))
    if user_id is None:
        return response(403)

    session = Session()

    card = session.query(CardModel).filter(
        CardModel.user_id == user_id
    ).filter(
        CardModel.card_id == card_id
    ).one_or_none()
    if card is not None:
        session.delete(card)
        session.commit()

    return response(204)
