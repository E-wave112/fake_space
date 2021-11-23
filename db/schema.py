from pydantic import BaseModel
from typing import Any, Dict, Optional,List


class UserCreate(BaseModel):
    email: Optional[str] = None
    title:str
    text:str
    subject:str
    prediction_score:int
    prediction:str 

    class Config:
        orm_mode = True