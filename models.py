from sqlalchemy import Column, Integer, String
from database import Base



class Output(Base):
    __tablename__ = "outputs"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    title = Column(String)
    text = Column(String)
    subject = Column(String)
    prediction = Column(Integer)
