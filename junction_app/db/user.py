from datetime import datetime

from sqlalchemy import Column, VARCHAR, BigInteger, DateTime

from db import Base


class UserModel(Base):
    __tablename__ = "user"
    user_id = Column(BigInteger, primary_key=True)
    username = Column(VARCHAR(45), nullable=False)
    password = Column(VARCHAR(255), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, username: str, password: str) -> None:
        self.username = username
        self.password = password
