from datetime import datetime

from sqlalchemy import Column, VARCHAR, BigInteger, DateTime, Date, Integer

from db import Base


class TeamModel(Base):
    __tablename__ = "team"
    team_id = Column(BigInteger, primary_key=True)
    team_name = Column(VARCHAR(255), nullable=False)
    password = Column(VARCHAR(255), nullable=False)
    game_date = Column(Date, nullable=True)
    goal_minute = Column(Integer, nullable=False)
    break_start_time = Column(DateTime, nullable=True)
    break_end_time = Column(DateTime, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, team_name: str, password: str, goal_minute: int) -> None:
        self.team_name = team_name
        self.password = password
        self.goal_minute = goal_minute
