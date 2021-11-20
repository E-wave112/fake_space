from fastapi import FastAPI,HTTPException,Query
from typing import Optional,List,Dict
from pydantic import BaseModel
from model import predict
from utils import tokenize_texts

tags_metadata= [{
        "name": "predict",
        "description": "Accepts a list(which consists of title,text and subject) and predicts whether \
        the news in question is genuine(1) or fake(0)"
}]


class NewsModel(BaseModel):
    title:str
    text:str
    subject:str

class PredictedModel(BaseModel):
    text:str
    prediction:int


app = FastAPI(
title="Fake News predictor",
    description="A Machine learning model built with FastAPI that predicts if a certain news is bogus(fake) or genuine",
    version="1.0.0",
    openapi_tags=tags_metadata
)


@app.post('/predict',status_code=200,tags=['predict'])
async def predict_model(text_inputs:NewsModel, email:Optional[str]=Query('joane@doe.com',min_length=3,max_length=100,regex="^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$")):
    # create an empty dictionary for the outputs
    outputs = dict()
    try:
    
        title = text_inputs.title
        text = text_inputs.text
        subject = text_inputs.subject
        # text_inputs:NewsModel

        # import the correct predictor
        args_dict = {"title":tokenize_texts([title]),"text":tokenize_texts([text]),"subject":tokenize_texts([subject])}
        prediction_res = predict(args_dict)
        # convert the predicted value to a list so that fastapi jsonable encode can return it as a response
        prediction_res_list = prediction_res.tolist()
        if prediction_res_list[0] == 1:
            outputs["score"] = 1
            outputs["status"] = "The news seems genuine"
        else:
            outputs["score"] = 0
            outputs["status"] = "The news seems fake"


        # if not prediction_res:
        #     raise HTTPException(status_code=404,detail="model not found")

        # PredictedModel.text = text
        # PredictedModel.prediction = prediction_res

        return outputs

    except HTTPException as h:
        print(h)
        return {"error":h}