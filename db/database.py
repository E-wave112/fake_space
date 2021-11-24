from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from decouple import config

##connect the db url
POSTGRES_DATABASE_URL = config("POSTGRES_URI")

##create the DB engine
engine = create_engine(
    POSTGRES_DATABASE_URL
).connect()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

##create a base model class which will be used later on in the models file
Base = declarative_base()
