from fastapi import FastAPI,HTTPException,Query
from typing import Optional,List,Dict
from pydantic import BaseModel
from decouple import config
import numpy as np
from model import joblib_load
import joblib
import dill
import sys

if sys.version_info[0] < 3: 
    from StringIO import StringIO # Python 2.x
    from BytesIO import BytesIO # Python 2.x
else:
    from io import StringIO,BytesIO # Python 3.x


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

class PredictedModel(BaseModel):
    text:str
    prediction:int


app = FastAPI(
 title="Fake News predictor",
    description="A Machine learning model built with FastAPI that predicts if a certain news is bogus(fake) or genuine",
    version="1.0.0",
    openapi_tags=tags_metadata
)



def predict(title,text,subject):
    ##load the joblib pretrained model from s3
    joblib_body=joblib_load['Body']
    joblib_obj=joblib_body.read()
    job_load_model=dill.load(BytesIO(joblib_obj))
    args_array = np.array([title,text,subject])
    text_predict=job_load_model.predict(args_array)
    return text_predict

# response_model=PredictedModel

@app.post('/predict',status_code=200,tags=['predict'])
async def predict_model(text_inputs:NewsModel, email:Optional[str]=Query('joane@doe.com',min_length=3,max_length=100,regex="^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$")):
    title = text_inputs.title
    text = text_inputs.text
    subject = text_inputs.subject

    labels_pred = np.array([title,text,subject])

    prediction_res = predict(title,text,subject)

    if not prediction_res:
        raise HTTPException(status_code=404,detail="model not found")

    # PredictedModel.text = text
    # PredictedModel.prediction = prediction_res

    return {"results":text}

