from sqlalchemy import Column, Integer, String,TIMESTAMP
from .database import Base



class Output(Base):
    __tablename__ = "outputs"

    instance_id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    title = Column(String)
    text = Column(String)
    subject = Column(String)
    prediction_score = Column(Integer)
    prediction = Column(String)
    dateCreated = Column(TIMESTAMP)