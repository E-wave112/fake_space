from sqlalchemy import Column, Integer, String, TIMESTAMP
import datetime

# from .database import Base
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Output(Base):
    __tablename__ = "outputs"

    instance_id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    title = Column(String)
    text = Column(String)
    subject = Column(String)
    prediction_score = Column(Integer)
    prediction = Column(String)
    dateCreated = Column(TIMESTAMP, default=datetime.datetime.utcnow())
