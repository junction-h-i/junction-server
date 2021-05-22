from datetime import datetime

from sqlalchemy import Column, VARCHAR, BigInteger, DateTime

from db import Base


class UserTeamMappingModel(Base):
    __tablename__ = "user_team_mapping"
    user_team_mapping_id = Column(BigInteger, primary_key=True)
    user_id = Column(BigInteger, nullable=False)
    team_id = Column(BigInteger, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, user_id: int, team_id: int) -> None:
        self.user_id = user_id
        self.team_id = team_id
