from sqlalchemy.orm import Session
from . import models, schema
import datetime


def add_user(db: Session, user: schema.UserCreate):
    new_user = models.Output(
        email=user["email"],
        title=user["title"],
        text=user["text"],
        subject=user["subject"],
        prediction_score=user["prediction_score"],
        prediction=user["prediction"],
        # dateCreated = datetime.datetime.utcnow()
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return f"user created: {new_user}"
