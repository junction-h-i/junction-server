from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from junction_app import DB_URL


engine = create_engine(DB_URL)
Base = declarative_base(bind=engine)
session = sessionmaker(bind=engine)

