from datetime import datetime

from sqlalchemy import Column, BigInteger, DateTime, VARCHAR, Text, Integer

from db import Base


class CardModel(Base):
    __tablename__ = "card"

    card_id = Column(BigInteger, primary_key=True)
    user_id = Column(BigInteger, nullable=False)
    team_id = Column(BigInteger, nullable=True),
    start_time = Column(DateTime, nullable=True)
    goal_focus_minute = Column(Integer, nullable=False)
    color = Column(VARCHAR(45), nullable=False)
    content = Column(Text, nullable=False)
    progress_status = Column(VARCHAR(45), nullable=False, default="TODO")
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, user_id: int, goal_focus_minute: int, color: str, content: str):
        self.user_id=user_id
        self.goal_focus_minute = goal_focus_minute
        self.color = color
        self.content = content
