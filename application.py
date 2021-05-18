from fastapi import FastAPI,HTTPException,Query
from typing import Optional,List,Dict
from pydantic import BaseModel
from decouple import config
from model import predict


##data fields 
##data_process = df[['title','text','subject']]
tags_metadata= [{
        "name": "predict",
        "description": "Accepts a list(which consists of title,text and subject) and predicts whether \
        the news in question is genuine(1) or fake(0)"
}]


class NewsModel(BaseModel):
    title:str
    text:str
    subject:str


app = FastAPI(
 title="Fake News predictor",
    description="A Machine learning model built with FastAPI that predicts if a certain news is bogus(fake) or genuine",
    version="1.0.0",
    openapi_tags=tags_metadata
)


@app.post('/predict',status_code=200,tags=['predict'])
async def predict_model(text_inputs:NewsModel,email:Optional[str]=Query('joane@doe.com',min_length=3,max_length=100,regex="^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$")):
    title = text_inputs.title
    text = text_inputs.text
    subject = text_inputs.subject

    prediction_res = predict([title,text,subject])

    if not prediction_res:
        raise HTTPException(status_code=404,detail="model not found")

    return {"results":prediction_res}

